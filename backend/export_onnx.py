import torch
from models.masking_net import AudioMaskingNet

# Load model
model = AudioMaskingNet()
model.load_state_dict(
    torch.load("../checkpoints/model.pt", map_location="cpu")
)

model.eval()

# Dummy input matching your model shape
dummy_input = torch.randn(1, 1, 257, 8)

# Export
torch.onnx.export(
    model,
    dummy_input,
    "../checkpoints/model.onnx",

    input_names=["input"],
    output_names=["output"],

    opset_version=18,
)

print("ONNX export complete")