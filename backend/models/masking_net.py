import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),

            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class AudioMaskingNet(nn.Module):
    def __init__(self):
        super().__init__()

        # Encoder
        self.enc1 = ConvBlock(1, 32)
        self.pool1 = nn.MaxPool2d(2)

        self.enc2 = ConvBlock(32, 64)
        self.pool2 = nn.MaxPool2d(2)

        self.enc3 = ConvBlock(64, 128)
        self.pool3 = nn.MaxPool2d(2)

        # Bottleneck
        self.bottleneck = ConvBlock(128, 256)

        # Decoder
        self.up3 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec3 = ConvBlock(256, 128)

        self.up2 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec2 = ConvBlock(128, 64)

        self.up1 = nn.ConvTranspose2d(64, 32, 2, stride=2)
        self.dec1 = ConvBlock(64, 32)

        # Output
        self.out = nn.Conv2d(32, 1, kernel_size=1)
        self.activation = nn.Sigmoid()

    def _match_size(self, src, target):
        """
        Ensures src tensor matches target spatial dims (F, T)
        Crops if larger, pads if smaller.
        """
        _, _, h, w = src.shape
        _, _, th, tw = target.shape

        # Crop if too big
        src = src[:, :, :th, :tw]

        # Pad if too small
        if src.shape[2] < th or src.shape[3] < tw:
            pad_h = th - src.shape[2]
            pad_w = tw - src.shape[3]
            src = nn.functional.pad(src, (0, pad_w, 0, pad_h))

        return src

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)                 # [B, 32, F, T]
        e2 = self.enc2(self.pool1(e1))    # [B, 64, F/2, T/2]
        e3 = self.enc3(self.pool2(e2))    # [B, 128, F/4, T/4]

        # Bottleneck
        b = self.bottleneck(self.pool3(e3))  # [B, 256, F/8, T/8]

        # Decoder + skip connections

        d3 = self.up3(b)
        e3 = self._match_size(e3, d3)
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.dec3(d3)

        d2 = self.up2(d3)
        e2 = self._match_size(e2, d2)
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)

        d1 = self.up1(d2)
        e1 = self._match_size(e1, d1)
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)

        out = self.out(d1)

        return self.activation(out)