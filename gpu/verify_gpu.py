"""Same GPU check for every route: versions, device, and a real computation."""
import platform
import sys
import time

import torch

print("torch          ", torch.__version__)
print("cuda runtime   ", torch.version.cuda)
print("cuda available ", torch.cuda.is_available())
if not torch.cuda.is_available():
    sys.exit("FAIL: CUDA is not available; this route did not reach the GPU")
print("device         ", torch.cuda.get_device_name(0))
print("capability     ", torch.cuda.get_device_capability(0))
torch.manual_seed(0)
a = torch.randn(4096, 4096, device="cuda")
b = torch.randn(4096, 4096, device="cuda")
torch.cuda.synchronize()
t0 = time.perf_counter()
c = a @ b
torch.cuda.synchronize()
print("matmul 4096^2  ", f"{time.perf_counter() - t0:.4f} s, checksum {c.sum().item():.4e}")
print("host           ", platform.platform())
