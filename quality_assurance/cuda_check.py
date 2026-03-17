import torch
print(f"Torch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name(0)}")

try:
    import torchvision
    print(f"Torchvision version: {torchvision.__version__}")
    from torchvision.ops import nms
    print("torchvision.ops.nms is available")
except Exception as e:
    print(f"Torchvision import or nms check failed: {e}")