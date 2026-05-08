import torch
import torch.nn as nn


criterion = nn.MSELoss()

def train_step(model, noisy_spec, clean_spec, optimizer, device):
    model.train()
    optimizer.zero_grad()

    # Move to device
    noisy_spec = noisy_spec.to(device)
    clean_spec = clean_spec.to(device)

    # Ensure correct shape: [B, 1, F, T]
    if noisy_spec.dim() == 3:
        noisy_spec = noisy_spec.unsqueeze(1)
        clean_spec = clean_spec.unsqueeze(1)

    # Ideal Ratio Mask
    target_mask = clean_spec / (noisy_spec + 1e-8)   #this is normalized ratio
    target_mask = torch.clamp(target_mask, 0.0, 1.0)

    noisy_spec = torch.log1p(noisy_spec)    #Log scaling

    #Forward
    output_mask = model(noisy_spec)

    #Matching target mask and output mask spatial sizes
    min_f = min(output_mask.shape[2], target_mask.shape[2])
    min_t = min(output_mask.shape[3], target_mask.shape[3])
    output_mask = output_mask[:, :, :min_f, :min_t]
    target_mask = target_mask[:, :, :min_f, :min_t]

    # Loss
    loss = criterion(output_mask, target_mask)

    # Backprop
    loss.backward()

    # Gradient clipping (stability)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

    optimizer.step()

    return loss.item()


def train(model, dataloader, optimizer, epochs=10, device="cpu"):
    model.to(device)

    for epoch in range(epochs):
        total_loss = 0.0

        for noisy, clean in dataloader:
            loss = train_step(model, noisy, clean, optimizer, device)
            total_loss += loss

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}: Avg Loss = {avg_loss:.6f}")