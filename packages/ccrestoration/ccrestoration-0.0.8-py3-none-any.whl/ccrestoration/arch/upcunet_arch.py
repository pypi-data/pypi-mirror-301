# type: ignore
import os

import torch
from torch import nn as nn
from torch.nn import functional as F

from ccrestoration.arch import ARCH_REGISTRY
from ccrestoration.type import ArchType


@ARCH_REGISTRY.register(name=ArchType.UPCUNET)
class UpCunet(nn.Module):
    """
    UpCunet model, which output is the normalized RGB image. (original output is the 0-255 RGB image)
    :: 输出修改为归一化的RGB图像，原始实现为输出为0-255的RGB图像

    增加了一层unet键，需要手动修改state_dict的键，添加"unet."前缀，如下：
    if cfg.pro:
        del state_dict["pro"]

    new_state_dict = {}
    for key, value in state_dict.items():
        # 修改键，添加"unet."前缀
        new_key = "unet." + key
        new_state_dict[new_key] = value


    cache_mode:
    0: 默认使用cache缓存必要参数
    1: 使用cache缓存必要参数，对缓存进行8bit量化节省显存，带来15%延时增长，肉眼完全无法感知的有损模式
    2: 不使用cache，有损模式。耗时约增加25%，仅在有景深虚化的图里有微小的误差，不影响纹理判断
    3: 不使用cache，无损模式。耗时约为默认模式的2.5倍，但是显存不受输入图像分辨率限制

    :param in_channels: The number of input channels. Default is 3.
    :param out_channels: The number of output channels. Default is 3.
    :param scale: The scale factor. Default is 2.
    :param cache_mode: The cache mode. Default is 0(0: use cache, 1: use cache and quantize cache to 8bit, 2: not use cache, 3: not use cache and without loss).
    :param alpha: The alpha value. Default is 1.
    :param pro: Pro model. Default is False.
    """

    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 3,
        scale: int = 2,
        cache_mode: int = 0,
        alpha: float = 1,
        pro: bool = False,
    ):
        super(UpCunet, self).__init__()
        if scale == 2:
            self.unet = UpCunet2x(in_channels, out_channels)
        elif scale == 3:
            self.unet = UpCunet3x(in_channels, out_channels)
        elif scale == 4:
            self.unet = UpCunet4x(in_channels, out_channels)
        else:
            raise ValueError("scale must be 2, 3 or 4")

        if cache_mode not in [0, 1, 2, 3]:
            raise ValueError("cache_mode must be 0, 1, 2 or 3")

        self.cache_mode = cache_mode
        self.alpha = alpha
        self.pro = pro

    def forward(self, x):
        if self.pro:
            x = x * 0.7 + 0.15

        if self.cache_mode == 3:
            return self.unet.forward_gap_sync(x=x, tile_mode=0, alpha=self.alpha, pro=self.pro)
        elif self.cache_mode == 2:
            return self.unet.forward_fast_rough(x=x, tile_mode=0, alpha=self.alpha, pro=self.pro)
        else:
            return self.unet.forward(x=x, tile_mode=0, cache_mode=self.cache_mode, alpha=self.alpha, pro=self.pro)


def q(inp, cache_mode):
    maxx = inp.max()
    minn = inp.min()
    delta = maxx - minn
    if cache_mode == 2:
        return (
            ((inp - minn) / delta * 255).round().byte().cpu(),
            delta,
            minn,
            inp.device,
        )  # 大概3倍延时#太慢了，屏蔽该模式
    elif cache_mode == 1:
        return ((inp - minn) / delta * 255).round().byte(), delta, minn, inp.device  # 不用CPU转移


def dq(inp, if_half, cache_mode, delta, minn, device):
    if cache_mode == 2:
        if if_half:
            return inp.to(device).half() / 255 * delta + minn
        else:
            return inp.to(device).float() / 255 * delta + minn
    elif cache_mode == 1:
        if if_half:
            return inp.half() / 255 * delta + minn  # 不用CPU转移
        else:
            return inp.float() / 255 * delta + minn


class SEBlock(nn.Module):
    def __init__(self, in_channels, reduction=8, bias=False):
        super(SEBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, in_channels // reduction, 1, 1, 0, bias=bias)
        self.conv2 = nn.Conv2d(in_channels // reduction, in_channels, 1, 1, 0, bias=bias)

    def forward(self, x):
        if "Half" in x.type():  # torch.HalfTensor/torch.cuda.HalfTensor
            x0 = torch.mean(x.float(), dim=(2, 3), keepdim=True).half()
        else:
            x0 = torch.mean(x, dim=(2, 3), keepdim=True)
        x0 = self.conv1(x0)
        x0 = F.relu(x0, inplace=True)
        x0 = self.conv2(x0)
        x0 = torch.sigmoid(x0)
        x = torch.mul(x, x0)
        return x

    def forward_mean(self, x, x0):
        x0 = self.conv1(x0)
        x0 = F.relu(x0, inplace=True)
        x0 = self.conv2(x0)
        x0 = torch.sigmoid(x0)
        x = torch.mul(x, x0)
        return x


class UNetConv(nn.Module):
    def __init__(self, in_channels, mid_channels, out_channels, se):
        super(UNetConv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, 3, 1, 0),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(mid_channels, out_channels, 3, 1, 0),
            nn.LeakyReLU(0.1, inplace=True),
        )
        if se:
            self.seblock = SEBlock(out_channels, reduction=8, bias=True)
        else:
            self.seblock = None

    def forward(self, x):
        z = self.conv(x)
        if self.seblock is not None:
            z = self.seblock(z)
        return z


class UNet1(nn.Module):
    def __init__(self, in_channels, out_channels, deconv):
        super(UNet1, self).__init__()
        self.conv1 = UNetConv(in_channels, 32, 64, se=False)
        self.conv1_down = nn.Conv2d(64, 64, 2, 2, 0)
        self.conv2 = UNetConv(64, 128, 64, se=True)
        self.conv2_up = nn.ConvTranspose2d(64, 64, 2, 2, 0)
        self.conv3 = nn.Conv2d(64, 64, 3, 1, 0)

        if deconv:
            self.conv_bottom = nn.ConvTranspose2d(64, out_channels, 4, 2, 3)
        else:
            self.conv_bottom = nn.Conv2d(64, out_channels, 3, 1, 0)

        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv1_down(x1)
        x1 = F.pad(x1, (-4, -4, -4, -4))
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x2 = self.conv2(x2)
        x2 = self.conv2_up(x2)
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x3 = self.conv3(x1 + x2)
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        z = self.conv_bottom(x3)
        return z

    def forward_a(self, x):
        x1 = self.conv1(x)
        x2 = self.conv1_down(x1)
        x1 = F.pad(x1, (-4, -4, -4, -4))
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x2 = self.conv2.conv(x2)
        return x1, x2

    def forward_b(self, x1, x2):
        x2 = self.conv2_up(x2)
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x3 = self.conv3(x1 + x2)
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        z = self.conv_bottom(x3)
        return z


class UNet1x3(nn.Module):
    def __init__(self, in_channels, out_channels, deconv):
        super(UNet1x3, self).__init__()
        self.conv1 = UNetConv(in_channels, 32, 64, se=False)
        self.conv1_down = nn.Conv2d(64, 64, 2, 2, 0)
        self.conv2 = UNetConv(64, 128, 64, se=True)
        self.conv2_up = nn.ConvTranspose2d(64, 64, 2, 2, 0)
        self.conv3 = nn.Conv2d(64, 64, 3, 1, 0)

        if deconv:
            self.conv_bottom = nn.ConvTranspose2d(64, out_channels, 5, 3, 2)
        else:
            self.conv_bottom = nn.Conv2d(64, out_channels, 3, 1, 0)

        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv1_down(x1)
        x1 = F.pad(x1, (-4, -4, -4, -4))
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x2 = self.conv2(x2)
        x2 = self.conv2_up(x2)
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x3 = self.conv3(x1 + x2)
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        z = self.conv_bottom(x3)
        return z

    def forward_a(self, x):
        x1 = self.conv1(x)
        x2 = self.conv1_down(x1)
        x1 = F.pad(x1, (-4, -4, -4, -4))
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x2 = self.conv2.conv(x2)
        return x1, x2

    def forward_b(self, x1, x2):
        x2 = self.conv2_up(x2)
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x3 = self.conv3(x1 + x2)
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        z = self.conv_bottom(x3)
        return z


class UNet2(nn.Module):
    def __init__(self, in_channels, out_channels, deconv):
        super(UNet2, self).__init__()

        self.conv1 = UNetConv(in_channels, 32, 64, se=False)
        self.conv1_down = nn.Conv2d(64, 64, 2, 2, 0)
        self.conv2 = UNetConv(64, 64, 128, se=True)
        self.conv2_down = nn.Conv2d(128, 128, 2, 2, 0)
        self.conv3 = UNetConv(128, 256, 128, se=True)
        self.conv3_up = nn.ConvTranspose2d(128, 128, 2, 2, 0)
        self.conv4 = UNetConv(128, 64, 64, se=True)
        self.conv4_up = nn.ConvTranspose2d(64, 64, 2, 2, 0)
        self.conv5 = nn.Conv2d(64, 64, 3, 1, 0)

        if deconv:
            self.conv_bottom = nn.ConvTranspose2d(64, out_channels, 4, 2, 3)
        else:
            self.conv_bottom = nn.Conv2d(64, out_channels, 3, 1, 0)

        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x, alpha=1):
        x1 = self.conv1(x)
        x2 = self.conv1_down(x1)
        x1 = F.pad(x1, (-16, -16, -16, -16))
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x2 = self.conv2(x2)
        x3 = self.conv2_down(x2)
        x2 = F.pad(x2, (-4, -4, -4, -4))
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        x3 = self.conv3(x3)
        x3 = self.conv3_up(x3)
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        x4 = self.conv4(x2 + x3)
        x4 *= alpha
        x4 = self.conv4_up(x4)
        x4 = F.leaky_relu(x4, 0.1, inplace=True)
        x5 = self.conv5(x1 + x4)
        x5 = F.leaky_relu(x5, 0.1, inplace=True)
        z = self.conv_bottom(x5)
        return z

    def forward_a(self, x):  # conv234结尾有se
        x1 = self.conv1(x)
        x2 = self.conv1_down(x1)
        x1 = F.pad(x1, (-16, -16, -16, -16))
        x2 = F.leaky_relu(x2, 0.1, inplace=True)
        x2 = self.conv2.conv(x2)
        return x1, x2

    def forward_b(self, x2):  # conv234结尾有se
        x3 = self.conv2_down(x2)
        x2 = F.pad(x2, (-4, -4, -4, -4))
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        x3 = self.conv3.conv(x3)
        return x2, x3

    def forward_c(self, x2, x3):  # conv234结尾有se
        x3 = self.conv3_up(x3)
        x3 = F.leaky_relu(x3, 0.1, inplace=True)
        x4 = self.conv4.conv(x2 + x3)
        return x4

    def forward_d(self, x1, x4):  # conv234结尾有se
        x4 = self.conv4_up(x4)
        x4 = F.leaky_relu(x4, 0.1, inplace=True)
        x5 = self.conv5(x1 + x4)
        x5 = F.leaky_relu(x5, 0.1, inplace=True)

        z = self.conv_bottom(x5)
        return z


class UpCunet2x(nn.Module):
    def __init__(self, in_channels=3, out_channels=3):
        super(UpCunet2x, self).__init__()
        self.unet1 = UNet1(in_channels, out_channels, deconv=True)
        self.unet2 = UNet2(in_channels, out_channels, deconv=False)

    def forward(self, x, tile_mode, cache_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        if tile_mode == 0:  # 不tile
            ph = ((h0 - 1) // 2 + 1) * 2
            pw = ((w0 - 1) // 2 + 1) * 2
            x = F.pad(x, (18, 18 + pw - w0, 18, 18 + ph - h0), "reflect")  # 需要保证被2整除
            x = self.unet1.forward(x)
            x0 = self.unet2.forward(x, alpha)
            x = F.pad(x, (-20, -20, -20, -20))
            x = torch.add(x0, x)
            if w0 != pw or h0 != ph:
                x = x[:, :, : h0 * 2, : w0 * 2]
            if pro:
                return (x - 0.15) / 0.7
            else:
                return x
        elif tile_mode == 1:  # 对长边减半
            if w0 >= h0:
                crop_size_w = ((w0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_h = (h0 - 1) // 2 * 2 + 2  # 能被2整除
            else:
                crop_size_h = ((h0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_w = (w0 - 1) // 2 * 2 + 2  # 能被2整除
            crop_size = (crop_size_h, crop_size_w)
        elif tile_mode >= 2:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            t2 = tile_mode * 2
            crop_size = (((h0 - 1) // t2 * t2 + t2) // tile_mode, ((w0 - 1) // t2 * t2 + t2) // tile_mode)
        else:
            print("tile_mode config error")
            os._exit(233)

        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (18, 18 + pw - w0, 18, 18 + ph - h0), "reflect")
        n, c, h, w = x.shape
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        n_patch = 0
        tmp_dict = {}
        for i in range(0, h - 36, crop_size[0]):
            tmp_dict[i] = {}
            for j in range(0, w - 36, crop_size[1]):
                x_crop = x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36]
                n, c1, h1, w1 = x_crop.shape
                tmp0, x_crop = self.unet1.forward_a(x_crop)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(x_crop, dim=(2, 3), keepdim=True)
                se_mean0 += tmp_se_mean
                n_patch += 1
                tmp_dict[i][j] = (tmp0, x_crop)
        se_mean0 /= n_patch
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = tmp_dict[i][j]
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                opt_unet1 = F.pad(opt_unet1, (-20, -20, -20, -20))
                if cache_mode:
                    opt_unet1, tmp_x1 = q(opt_unet1, cache_mode), q(tmp_x1, cache_mode)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x2 = q(tmp_x2, cache_mode)
                se_mean1 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x2)
        se_mean1 /= n_patch
        if if_half:
            se_mean0 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                opt_unet1, tmp_x1, tmp_x2 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x2 = dq(tmp_x2[0], if_half, cache_mode, tmp_x2[1], tmp_x2[2], tmp_x2[3])
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if cache_mode:
                    tmp_x2 = q(tmp_x2, cache_mode)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x3 = q(tmp_x3, cache_mode)
                se_mean0 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x2, tmp_x3)
        se_mean0 /= n_patch
        if if_half:
            se_mean1 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                opt_unet1, tmp_x1, tmp_x2, tmp_x3 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x3 = dq(tmp_x3[0], if_half, cache_mode, tmp_x3[1], tmp_x3[2], tmp_x3[3])
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean0)
                if cache_mode:
                    tmp_x2 = dq(tmp_x2[0], if_half, cache_mode, tmp_x2[1], tmp_x2[2], tmp_x2[3])
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x4 = q(tmp_x4, cache_mode)
                se_mean1 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x4)
        se_mean1 /= n_patch
        res = torch.zeros((n, c, h * 2 - 72, w * 2 - 72), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                x, tmp_x1, tmp_x4 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x4 = dq(tmp_x4[0], if_half, cache_mode, tmp_x4[1], tmp_x4[2], tmp_x4[3])
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean1)
                if cache_mode:
                    tmp_x1 = dq(tmp_x1[0], if_half, cache_mode, tmp_x1[1], tmp_x1[2], tmp_x1[3])
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                if cache_mode:
                    x = dq(x[0], if_half, cache_mode, x[1], x[2], x[3])
                del tmp_dict[i][j]
                x = torch.add(x0, x)  # x0是unet2的最终输出
                if pro:
                    res[:, :, i * 2 : i * 2 + h1 * 2 - 72, j * 2 : j * 2 + w1 * 2 - 72] = (x - 0.15) / 0.7
                else:
                    res[:, :, i * 2 : i * 2 + h1 * 2 - 72, j * 2 : j * 2 + w1 * 2 - 72] = x
        del tmp_dict
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 2, : w0 * 2]
        return res

    def forward_gap_sync(self, x, tile_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        if tile_mode == 0:  # 不tile
            ph = ((h0 - 1) // 2 + 1) * 2
            pw = ((w0 - 1) // 2 + 1) * 2
            x = F.pad(x, (18, 18 + pw - w0, 18, 18 + ph - h0), "reflect")  # 需要保证被2整除
            x = self.unet1.forward(x)
            x0 = self.unet2.forward(x, alpha)
            x = F.pad(x, (-20, -20, -20, -20))
            x = torch.add(x0, x)
            if w0 != pw or h0 != ph:
                x = x[:, :, : h0 * 2, : w0 * 2]
            if pro:
                return (x - 0.15) / 0.7
            else:
                return x
        elif tile_mode == 1:  # 对长边减半
            if w0 >= h0:
                crop_size_w = ((w0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_h = (h0 - 1) // 2 * 2 + 2  # 能被2整除
            else:
                crop_size_h = ((h0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_w = (w0 - 1) // 2 * 2 + 2  # 能被2整除
            crop_size = (crop_size_h, crop_size_w)  # 6.6G
        elif tile_mode >= 2:  # hw都减半
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            t2 = tile_mode * 2
            crop_size = (((h0 - 1) // t2 * t2 + t2) // tile_mode, ((w0 - 1) // t2 * t2 + t2) // tile_mode)
        else:
            print("tile_mode config error")
            os._exit(233)
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (18, 18 + pw - w0, 18, 18 + ph - h0), "reflect")
        n, c, h, w = x.shape
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        n_patch = 0
        h1, w1 = crop_size[0] + 36, crop_size[1] + 36
        ######stage1
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(x_crop, dim=(2, 3), keepdim=True)
                se_mean0 += tmp_se_mean
                n_patch += 1
        se_mean0 /= n_patch
        ######stage1+state2
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                se_mean1 += tmp_se_mean
        se_mean1 /= n_patch
        ######stage1+state2+state3
        if if_half:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                se_mean2 += tmp_se_mean
        se_mean2 /= n_patch
        #########stage1+state2+state3+stage4
        if if_half:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean3 = se_mean3.half()
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
                se_mean3 += tmp_se_mean
        se_mean3 /= n_patch
        ###########stage1+state2+state3+stage4+stage_tail
        res = torch.zeros((n, c, h * 2 - 72, w * 2 - 72), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                x_crop = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(x_crop)
                x_crop = F.pad(x_crop, (-20, -20, -20, -20))
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean3)
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                x_crop = torch.add(x0, x_crop)
                if pro:
                    res[:, :, i * 2 : i * 2 + h1 * 2 - 72, j * 2 : j * 2 + w1 * 2 - 72] = (x_crop - 0.15) / 0.7
                else:
                    res[:, :, i * 2 : i * 2 + h1 * 2 - 72, j * 2 : j * 2 + w1 * 2 - 72] = x_crop
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 2, : w0 * 2]
        return res

    def forward_fast_rough(self, x, tile_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        if tile_mode < 3:
            return self.forward(x, tile_mode, 1, alpha, pro)  # 至少切成3x3
        elif tile_mode >= 3:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            if tile_mode < 3:
                return self.forward(x, tile_mode, 1, alpha, pro)
            t2 = tile_mode * 2
            crop_size = (((h0 - 1) // t2 * t2 + t2) // tile_mode, ((w0 - 1) // t2 * t2 + t2) // tile_mode)
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (18, 18 + pw - w0, 18, 18 + ph - h0), "reflect")
        n, c, h, w = x.shape
        h1, w1 = crop_size[0] + 36, crop_size[1] + 36
        n_patch = 0
        ###########stage1+state2+state3+stage4
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 36, crop_size[0]):
            if (i // crop_size[0]) % 2 == 0:
                continue
            for j in range(0, w - 36, crop_size[1]):
                if (j // crop_size[1]) % 2 == 0:
                    continue
                n_patch += 1
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                if if_half:
                    se_mean0 += torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean0 += torch.mean(x_crop, dim=(2, 3), keepdim=True)
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0 / n_patch)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                if if_half:
                    se_mean1 += torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean1 += torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1 / n_patch)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if if_half:
                    se_mean2 += torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean2 += torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2 / n_patch)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                if if_half:
                    se_mean3 += torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean3 += torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
        # print("2x-n_patch=%s,tile_mode=%s" % (n_patch,tile_mode))
        ###########stage1+state2+state3+stage4+stage_tail
        res = torch.zeros((n, c, h * 2 - 72, w * 2 - 72), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 36, crop_size[0]):
            for j in range(0, w - 36, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 36, j : j + crop_size[1] + 36])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0 / n_patch)
                x_crop = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(x_crop)
                x_crop = F.pad(x_crop, (-20, -20, -20, -20))
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1 / n_patch)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2 / n_patch)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean3 / n_patch)
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                x_crop = torch.add(x0, x_crop)
                if pro:
                    res[:, :, i * 2 : i * 2 + h1 * 2 - 72, j * 2 : j * 2 + w1 * 2 - 72] = (x_crop - 0.15) / 0.7
                else:
                    res[:, :, i * 2 : i * 2 + h1 * 2 - 72, j * 2 : j * 2 + w1 * 2 - 72] = x_crop
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 2, : w0 * 2]
        return res


class UpCunet3x(nn.Module):
    def __init__(self, in_channels=3, out_channels=3):
        super(UpCunet3x, self).__init__()
        self.unet1 = UNet1x3(in_channels, out_channels, deconv=True)
        self.unet2 = UNet2(in_channels, out_channels, deconv=False)

    def forward(self, x, tile_mode, cache_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        if tile_mode == 0:  # 不tile
            ph = ((h0 - 1) // 4 + 1) * 4
            pw = ((w0 - 1) // 4 + 1) * 4
            x = F.pad(x, (14, 14 + pw - w0, 14, 14 + ph - h0), "reflect")  # 需要保证被2整除
            x = self.unet1.forward(x)
            x0 = self.unet2.forward(x, alpha)
            x = F.pad(x, (-20, -20, -20, -20))
            x = torch.add(x0, x)
            if w0 != pw or h0 != ph:
                x = x[:, :, : h0 * 3, : w0 * 3]
            if pro:
                return (x - 0.15) / 0.7
            else:
                return x
        elif tile_mode == 1:  # 对长边减半
            if w0 >= h0:
                crop_size_w = ((w0 - 1) // 8 * 8 + 8) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_h = (h0 - 1) // 4 * 4 + 4  # 能被2整除
            else:
                crop_size_h = ((h0 - 1) // 8 * 8 + 8) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_w = (w0 - 1) // 4 * 4 + 4  # 能被2整除
            crop_size = (crop_size_h, crop_size_w)
        elif tile_mode >= 2:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            t4 = tile_mode * 4
            crop_size = (((h0 - 1) // t4 * t4 + t4) // tile_mode, ((w0 - 1) // t4 * t4 + t4) // tile_mode)
        else:
            print("tile_mode config error")
            os._exit(233)
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (14, 14 + pw - w0, 14, 14 + ph - h0), "reflect")
        n, c, h, w = x.shape
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        n_patch = 0
        tmp_dict = {}
        for i in range(0, h - 28, crop_size[0]):
            tmp_dict[i] = {}
            for j in range(0, w - 28, crop_size[1]):
                x_crop = x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28]
                n, c1, h1, w1 = x_crop.shape
                tmp0, x_crop = self.unet1.forward_a(x_crop)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(x_crop, dim=(2, 3), keepdim=True)
                se_mean0 += tmp_se_mean
                n_patch += 1
                tmp_dict[i][j] = (tmp0, x_crop)
        se_mean0 /= n_patch
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = tmp_dict[i][j]
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                opt_unet1 = F.pad(opt_unet1, (-20, -20, -20, -20))
                if cache_mode:
                    opt_unet1, tmp_x1 = q(opt_unet1, cache_mode), q(tmp_x1, cache_mode)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x2 = q(tmp_x2, cache_mode)
                se_mean1 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x2)
        se_mean1 /= n_patch
        if if_half:
            se_mean0 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                opt_unet1, tmp_x1, tmp_x2 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x2 = dq(tmp_x2[0], if_half, cache_mode, tmp_x2[1], tmp_x2[2], tmp_x2[3])
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if cache_mode:
                    tmp_x2 = q(tmp_x2, cache_mode)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x3 = q(tmp_x3, cache_mode)
                se_mean0 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x2, tmp_x3)
        se_mean0 /= n_patch
        if if_half:
            se_mean1 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                opt_unet1, tmp_x1, tmp_x2, tmp_x3 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x3 = dq(tmp_x3[0], if_half, cache_mode, tmp_x3[1], tmp_x3[2], tmp_x3[3])
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean0)
                if cache_mode:
                    tmp_x2 = dq(tmp_x2[0], if_half, cache_mode, tmp_x2[1], tmp_x2[2], tmp_x2[3])
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x4 = q(tmp_x4, cache_mode)
                se_mean1 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x4)
        se_mean1 /= n_patch
        res = torch.zeros((n, c, h * 3 - 84, w * 3 - 84), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                x, tmp_x1, tmp_x4 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x4 = dq(tmp_x4[0], if_half, cache_mode, tmp_x4[1], tmp_x4[2], tmp_x4[3])
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean1)
                if cache_mode:
                    tmp_x1 = dq(tmp_x1[0], if_half, cache_mode, tmp_x1[1], tmp_x1[2], tmp_x1[3])
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                if cache_mode:
                    x = dq(x[0], if_half, cache_mode, x[1], x[2], x[3])
                del tmp_dict[i][j]
                x = torch.add(x0, x)  # x0是unet2的最终输出
                if pro:
                    res[:, :, i * 3 : i * 3 + h1 * 3 - 84, j * 3 : j * 3 + w1 * 3 - 84] = (x - 0.15) / 0.7
                else:
                    res[:, :, i * 3 : i * 3 + h1 * 3 - 84, j * 3 : j * 3 + w1 * 3 - 84] = x
        del tmp_dict
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 3, : w0 * 3]
        return res

    def forward_gap_sync(self, x, tile_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        if tile_mode == 0:  # 不tile
            ph = ((h0 - 1) // 4 + 1) * 4
            pw = ((w0 - 1) // 4 + 1) * 4
            x = F.pad(x, (14, 14 + pw - w0, 14, 14 + ph - h0), "reflect")  # 需要保证被2整除
            x = self.unet1.forward(x)
            x0 = self.unet2.forward(x, alpha)
            x = F.pad(x, (-20, -20, -20, -20))
            x = torch.add(x0, x)
            if w0 != pw or h0 != ph:
                x = x[:, :, : h0 * 3, : w0 * 3]
            if pro:
                return (x - 0.15) / 0.7
            else:
                return x
        elif tile_mode == 1:  # 对长边减半
            if w0 >= h0:
                crop_size_w = ((w0 - 1) // 8 * 8 + 8) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_h = (h0 - 1) // 4 * 4 + 4  # 能被2整除
            else:
                crop_size_h = ((h0 - 1) // 8 * 8 + 8) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_w = (w0 - 1) // 4 * 4 + 4  # 能被2整除
            crop_size = (crop_size_h, crop_size_w)
        elif tile_mode >= 2:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            t4 = tile_mode * 4
            crop_size = (((h0 - 1) // t4 * t4 + t4) // tile_mode, ((w0 - 1) // t4 * t4 + t4) // tile_mode)
        else:
            print("tile_mode config error")
            os._exit(233)
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (14, 14 + pw - w0, 14, 14 + ph - h0), "reflect")
        n, c, h, w = x.shape
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        n_patch = 0
        h1, w1 = crop_size[0] + 28, crop_size[1] + 28
        ######stage1
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(x_crop, dim=(2, 3), keepdim=True)
                se_mean0 += tmp_se_mean
                n_patch += 1
        se_mean0 /= n_patch
        ######stage1+state2
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                se_mean1 += tmp_se_mean
        se_mean1 /= n_patch
        ######stage1+state2+state3
        if if_half:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                se_mean2 += tmp_se_mean
        se_mean2 /= n_patch
        #########stage1+state2+state3+stage4
        if if_half:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
                se_mean3 += tmp_se_mean
        se_mean3 /= n_patch
        ###########stage1+state2+state3+stage4+stage_tail
        res = torch.zeros((n, c, h * 3 - 84, w * 3 - 84), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                x_crop = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(x_crop)
                x_crop = F.pad(x_crop, (-20, -20, -20, -20))
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean3)
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                x_crop = torch.add(x0, x_crop)
                if pro:
                    res[:, :, i * 3 : i * 3 + h1 * 3 - 84, j * 3 : j * 3 + w1 * 3 - 84] = (x_crop - 0.15) / 0.7
                else:
                    res[:, :, i * 3 : i * 3 + h1 * 3 - 84, j * 3 : j * 3 + w1 * 3 - 84] = x_crop
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 3, : w0 * 3]
        return res

    def forward_fast_rough(self, x, tile_mode, alpha, pro):  # 1.7G
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        if tile_mode < 3:
            return self.forward(x, tile_mode, 1, alpha, pro)  # 至少切成3x3
        elif tile_mode >= 3:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            if tile_mode < 3:
                return self.forward(x, tile_mode, 1, alpha, pro)
            t4 = tile_mode * 4
            crop_size = (((h0 - 1) // t4 * t4 + t4) // tile_mode, ((w0 - 1) // t4 * t4 + t4) // tile_mode)  # 5.6G
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (14, 14 + pw - w0, 14, 14 + ph - h0), "reflect")
        n, c, h, w = x.shape
        h1, w1 = crop_size[0] + 28, crop_size[1] + 28
        n_patch = 0
        ###########stage1+state2+state3+stage4
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 28, crop_size[0]):
            if (i // crop_size[0]) % 2 == 0:
                continue
            for j in range(0, w - 28, crop_size[1]):
                if (j // crop_size[1]) % 2 == 0:
                    continue
                n_patch += 1
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                if if_half:
                    se_mean0 += torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean0 += torch.mean(x_crop, dim=(2, 3), keepdim=True)
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0 / n_patch)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                if if_half:
                    se_mean1 += torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean1 += torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1 / n_patch)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if if_half:
                    se_mean2 += torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean2 += torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2 / n_patch)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                if if_half:
                    se_mean3 += torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean3 += torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
        # print("3x-n_patch=%s,tile_mode=%s" % (n_patch,tile_mode))
        ###########stage1+state2+state3+stage4+stage_tail
        res = torch.zeros((n, c, h * 3 - 84, w * 3 - 84), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 28, crop_size[0]):
            for j in range(0, w - 28, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 28, j : j + crop_size[1] + 28])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0 / n_patch)
                x_crop = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(x_crop)
                x_crop = F.pad(x_crop, (-20, -20, -20, -20))
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1 / n_patch)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2 / n_patch)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean3 / n_patch)
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                x_crop = torch.add(x0, x_crop)
                if pro:
                    res[:, :, i * 3 : i * 3 + h1 * 3 - 84, j * 3 : j * 3 + w1 * 3 - 84] = (x_crop - 0.15) / 0.7
                else:
                    res[:, :, i * 3 : i * 3 + h1 * 3 - 84, j * 3 : j * 3 + w1 * 3 - 84] = x_crop
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 3, : w0 * 3]
        return res


class UpCunet4x(nn.Module):
    def __init__(self, in_channels=3, out_channels=3):
        super(UpCunet4x, self).__init__()
        self.unet1 = UNet1(in_channels, 64, deconv=True)
        self.unet2 = UNet2(64, 64, deconv=False)
        self.ps = nn.PixelShuffle(2)
        self.conv_final = nn.Conv2d(64, 12, 3, 1, padding=0, bias=True)

    def forward(self, x, tile_mode, cache_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        x00 = x
        if tile_mode == 0:  # 不tile
            ph = ((h0 - 1) // 2 + 1) * 2
            pw = ((w0 - 1) // 2 + 1) * 2
            x = F.pad(x, (19, 19 + pw - w0, 19, 19 + ph - h0), "reflect")  # 需要保证被2整除
            x = self.unet1.forward(x)
            x0 = self.unet2.forward(x, alpha)
            x1 = F.pad(x, (-20, -20, -20, -20))
            x = torch.add(x0, x1)
            x = self.conv_final(x)
            x = F.pad(x, (-1, -1, -1, -1))
            x = self.ps(x)
            if w0 != pw or h0 != ph:
                x = x[:, :, : h0 * 4, : w0 * 4]
            x += F.interpolate(x00, scale_factor=4, mode="nearest")
            if pro:
                return (x - 0.15) / 0.7
            else:
                return x
        elif tile_mode == 1:  # 对长边减半
            if w0 >= h0:
                crop_size_w = ((w0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_h = (h0 - 1) // 2 * 2 + 2  # 能被2整除
            else:
                crop_size_h = ((h0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_w = (w0 - 1) // 2 * 2 + 2  # 能被2整除
            crop_size = (crop_size_h, crop_size_w)
        elif tile_mode >= 2:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            t2 = tile_mode * 2
            crop_size = (((h0 - 1) // t2 * t2 + t2) // tile_mode, ((w0 - 1) // t2 * t2 + t2) // tile_mode)
        else:
            print("tile_mode config error")
            os._exit(233)
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (19, 19 + pw - w0, 19, 19 + ph - h0), "reflect")
        n, c, h, w = x.shape
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        n_patch = 0
        tmp_dict = {}
        for i in range(0, h - 38, crop_size[0]):
            tmp_dict[i] = {}
            for j in range(0, w - 38, crop_size[1]):
                x_crop = x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38]
                n, c1, h1, w1 = x_crop.shape
                tmp0, x_crop = self.unet1.forward_a(x_crop)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(x_crop, dim=(2, 3), keepdim=True)
                se_mean0 += tmp_se_mean
                n_patch += 1
                tmp_dict[i][j] = (tmp0, x_crop)
        se_mean0 /= n_patch
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = tmp_dict[i][j]
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                opt_unet1 = F.pad(opt_unet1, (-20, -20, -20, -20))
                if cache_mode:
                    opt_unet1, tmp_x1 = q(opt_unet1, cache_mode), q(tmp_x1, cache_mode)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x2 = q(tmp_x2, cache_mode)
                se_mean1 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x2)
        se_mean1 /= n_patch
        if if_half:
            se_mean0 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                opt_unet1, tmp_x1, tmp_x2 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x2 = dq(tmp_x2[0], if_half, cache_mode, tmp_x2[1], tmp_x2[2], tmp_x2[3])
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if cache_mode:
                    tmp_x2 = q(tmp_x2, cache_mode)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x3 = q(tmp_x3, cache_mode)
                se_mean0 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x2, tmp_x3)
        se_mean0 /= n_patch
        if if_half:
            se_mean1 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                opt_unet1, tmp_x1, tmp_x2, tmp_x3 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x3 = dq(tmp_x3[0], if_half, cache_mode, tmp_x3[1], tmp_x3[2], tmp_x3[3])
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean0)
                if cache_mode:
                    tmp_x2 = dq(tmp_x2[0], if_half, cache_mode, tmp_x2[1], tmp_x2[2], tmp_x2[3])
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
                if cache_mode:
                    tmp_x4 = q(tmp_x4, cache_mode)
                se_mean1 += tmp_se_mean
                tmp_dict[i][j] = (opt_unet1, tmp_x1, tmp_x4)
        se_mean1 /= n_patch
        res = torch.zeros((n, c, h * 4 - 152, w * 4 - 152), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                x, tmp_x1, tmp_x4 = tmp_dict[i][j]
                if cache_mode:
                    tmp_x4 = dq(tmp_x4[0], if_half, cache_mode, tmp_x4[1], tmp_x4[2], tmp_x4[3])
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean1)
                if cache_mode:
                    tmp_x1 = dq(tmp_x1[0], if_half, cache_mode, tmp_x1[1], tmp_x1[2], tmp_x1[3])
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                del tmp_x1, tmp_x4
                if cache_mode:
                    x = dq(x[0], if_half, cache_mode, x[1], x[2], x[3])
                del tmp_dict[i][j]
                x = torch.add(x0, x)  # x0是unet2的最终输出
                x = self.conv_final(x)
                x = F.pad(x, (-1, -1, -1, -1))
                x = self.ps(x)
                x00_crop = x00[:, :, i : i + h1 - 38, j : j + w1 - 38]
                _, _, h2, w2 = x00_crop.shape
                x[:, :, : h2 * 4, : w2 * 4] += F.interpolate(x00_crop, scale_factor=4, mode="nearest")
                if pro:
                    res[:, :, i * 4 : i * 4 + h1 * 4 - 152, j * 4 : j * 4 + w1 * 4 - 152] = (x - 0.15) / 0.7
                else:
                    res[:, :, i * 4 : i * 4 + h1 * 4 - 152, j * 4 : j * 4 + w1 * 4 - 152] = x
        del tmp_dict
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 4, : w0 * 4]
        return res

    def forward_gap_sync(self, x, tile_mode, alpha, pro):
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        x00 = x
        if tile_mode == 0:  # 不tile
            ph = ((h0 - 1) // 2 + 1) * 2
            pw = ((w0 - 1) // 2 + 1) * 2
            x = F.pad(x, (19, 19 + pw - w0, 19, 19 + ph - h0), "reflect")  # 需要保证被2整除
            x = self.unet1.forward(x)
            x0 = self.unet2.forward(x, alpha)
            x1 = F.pad(x, (-20, -20, -20, -20))
            x = torch.add(x0, x1)
            x = self.conv_final(x)
            x = F.pad(x, (-1, -1, -1, -1))
            x = self.ps(x)
            if w0 != pw or h0 != ph:
                x = x[:, :, : h0 * 4, : w0 * 4]
            x += F.interpolate(x00, scale_factor=4, mode="nearest")
            if pro:
                return (x - 0.15) / 0.7
            else:
                return x
        elif tile_mode == 1:  # 对长边减半
            if w0 >= h0:
                crop_size_w = ((w0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_h = (h0 - 1) // 2 * 2 + 2  # 能被2整除
            else:
                crop_size_h = ((h0 - 1) // 4 * 4 + 4) // 2  # 减半后能被2整除，所以要先被4整除
                crop_size_w = (w0 - 1) // 2 * 2 + 2  # 能被2整除
            crop_size = (crop_size_h, crop_size_w)
        elif tile_mode >= 2:  # hw都减半
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            t2 = tile_mode * 2
            crop_size = (((h0 - 1) // t2 * t2 + t2) // tile_mode, ((w0 - 1) // t2 * t2 + t2) // tile_mode)  # 5.6G
        else:
            print("tile_mode config error")
            os._exit(233)
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (19, 19 + pw - w0, 19, 19 + ph - h0), "reflect")
        n, c, h, w = x.shape
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        n_patch = 0
        h1, w1 = crop_size[0] + 38, crop_size[1] + 38
        ######stage1
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(x_crop, dim=(2, 3), keepdim=True)
                se_mean0 += tmp_se_mean
                n_patch += 1
        se_mean0 /= n_patch
        ######stage1+state2
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                se_mean1 += tmp_se_mean
        se_mean1 /= n_patch
        ######stage1+state2+state3
        if if_half:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                se_mean2 += tmp_se_mean
        se_mean2 /= n_patch
        #########stage1+state2+state3+stage4
        if if_half:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                if if_half:  # torch.HalfTensor/torch.cuda.HalfTensor
                    tmp_se_mean = torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    tmp_se_mean = torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
                se_mean3 += tmp_se_mean
        se_mean3 /= n_patch
        ###########stage1+state2+state3+stage4+stage_tail
        res = torch.zeros((n, c, h * 4 - 152, w * 4 - 152), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0)
                x_crop = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(x_crop)
                x_crop = F.pad(x_crop, (-20, -20, -20, -20))
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean3)
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                x_crop = torch.add(x0, x_crop)
                x_crop = self.conv_final(x_crop)
                x_crop = F.pad(x_crop, (-1, -1, -1, -1))
                x_crop = self.ps(x_crop)
                x00_crop = x00[:, :, i : i + h1 - 38, j : j + w1 - 38]
                _, _, h2, w2 = x00_crop.shape
                x_crop[:, :, : h2 * 4, : w2 * 4] += F.interpolate(x00_crop, scale_factor=4, mode="nearest")
                if pro:
                    res[:, :, i * 4 : i * 4 + h1 * 4 - 152, j * 4 : j * 4 + w1 * 4 - 152] = (x_crop - 0.15) / 0.7
                else:
                    res[:, :, i * 4 : i * 4 + h1 * 4 - 152, j * 4 : j * 4 + w1 * 4 - 152] = x_crop
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 4, : w0 * 4]
        return res

    def forward_fast_rough(self, x, tile_mode, alpha, pro):  # 1.7G
        n, c, h0, w0 = x.shape
        if "Half" in x.type():
            if_half = True
        else:
            if_half = False
        x00 = x
        if tile_mode < 3:
            return self.forward(x, tile_mode, 1, alpha, pro)  # 至少切成3x3
        elif tile_mode >= 3:
            tile_mode = min(min(h0, w0) // 128, int(tile_mode))  # 最小短边为128*128
            if tile_mode < 3:
                return self.forward(x, tile_mode, 1, alpha, pro)
            t2 = tile_mode * 2
            crop_size = (((h0 - 1) // t2 * t2 + t2) // tile_mode, ((w0 - 1) // t2 * t2 + t2) // tile_mode)  # 5.6G
        ph = ((h0 - 1) // crop_size[0] + 1) * crop_size[0]
        pw = ((w0 - 1) // crop_size[1] + 1) * crop_size[1]
        x = F.pad(x, (19, 19 + pw - w0, 19, 19 + ph - h0), "reflect")
        n, c, h, w = x.shape
        h1, w1 = crop_size[0] + 38, crop_size[1] + 38
        n_patch = 0
        ###########stage1+state2+state3+stage4
        if if_half:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean0 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean1 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean2 = torch.zeros((n, 128, 1, 1), device=x.device, dtype=torch.float32)
        if if_half:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float16)
        else:
            se_mean3 = torch.zeros((n, 64, 1, 1), device=x.device, dtype=torch.float32)
        for i in range(0, h - 38, crop_size[0]):
            if (i // crop_size[0]) % 2 == 0:
                continue
            for j in range(0, w - 38, crop_size[1]):
                if (j // crop_size[1]) % 2 == 0:
                    continue
                n_patch += 1
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                if if_half:
                    se_mean0 += torch.mean(x_crop.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean0 += torch.mean(x_crop, dim=(2, 3), keepdim=True)
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0 / n_patch)
                opt_unet1 = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(opt_unet1)
                if if_half:
                    se_mean1 += torch.mean(tmp_x2.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean1 += torch.mean(tmp_x2, dim=(2, 3), keepdim=True)
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1 / n_patch)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                if if_half:
                    se_mean2 += torch.mean(tmp_x3.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean2 += torch.mean(tmp_x3, dim=(2, 3), keepdim=True)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2 / n_patch)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3)
                if if_half:
                    se_mean3 += torch.mean(tmp_x4.float(), dim=(2, 3), keepdim=True).half()
                else:
                    se_mean3 += torch.mean(tmp_x4, dim=(2, 3), keepdim=True)
        # print("4x-n_patch=%s,tile_mode=%s" % (n_patch,tile_mode))
        ###########stage1+state2+state3+stage4+stage_tail
        res = torch.zeros((n, c, h * 4 - 152, w * 4 - 152), dtype=torch.uint8, device=x.device)
        for i in range(0, h - 38, crop_size[0]):
            for j in range(0, w - 38, crop_size[1]):
                tmp0, x_crop = self.unet1.forward_a(x[:, :, i : i + crop_size[0] + 38, j : j + crop_size[1] + 38])
                x_crop = self.unet1.conv2.seblock.forward_mean(x_crop, se_mean0 / n_patch)
                x_crop = self.unet1.forward_b(tmp0, x_crop)
                tmp_x1, tmp_x2 = self.unet2.forward_a(x_crop)
                x_crop = F.pad(x_crop, (-20, -20, -20, -20))
                tmp_x2 = self.unet2.conv2.seblock.forward_mean(tmp_x2, se_mean1 / n_patch)
                tmp_x2, tmp_x3 = self.unet2.forward_b(tmp_x2)
                tmp_x3 = self.unet2.conv3.seblock.forward_mean(tmp_x3, se_mean2 / n_patch)
                tmp_x4 = self.unet2.forward_c(tmp_x2, tmp_x3) * alpha
                tmp_x4 = self.unet2.conv4.seblock.forward_mean(tmp_x4, se_mean3 / n_patch)
                x0 = self.unet2.forward_d(tmp_x1, tmp_x4)
                x_crop = torch.add(x0, x_crop)
                x_crop = self.conv_final(x_crop)
                x_crop = F.pad(x_crop, (-1, -1, -1, -1))
                x_crop = self.ps(x_crop)
                x00_crop = x00[:, :, i : i + h1 - 38, j : j + w1 - 38]
                _, _, h2, w2 = x00_crop.shape
                x_crop[:, :, : h2 * 4, : w2 * 4] += F.interpolate(x00_crop, scale_factor=4, mode="nearest")
                if pro:
                    res[:, :, i * 4 : i * 4 + h1 * 4 - 152, j * 4 : j * 4 + w1 * 4 - 152] = (x_crop - 0.15) / 0.7
                else:
                    res[:, :, i * 4 : i * 4 + h1 * 4 - 152, j * 4 : j * 4 + w1 * 4 - 152] = x_crop
        # torch.cuda.empty_cache()
        if w0 != pw or h0 != ph:
            res = res[:, :, : h0 * 4, : w0 * 4]
        return res
