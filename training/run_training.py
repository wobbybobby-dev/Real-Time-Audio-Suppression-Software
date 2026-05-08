import torch
from torch.utils.data import DataLoader

from training.dataset import SpeechNoiseDataset
from training.train_masker import train
from backend.models.masking_net import AudioMaskingNet

def main():
    dataset = SpeechNoiseDataset(
        speech_dir="data/clean",
        noise_dir="data/noise"
    )

    dataloader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=True,
        num_workers=0
    )

    model = AudioMaskingNet()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=1e-3
    )

    train(
        model,
        dataloader,
        optimizer,
        epochs=3,
        device="cpu"
    )

    torch.save(model.state_dict(), "checkpoints/model.pt")


if __name__ == "__main__":
    main()