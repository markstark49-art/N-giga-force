import torch
import time

device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
dtype  = torch.float16

# Maximo teorico calculado matematicamente:
# VRAM_USABLE = (8192 - 512) MB = 7680 MB = 8,053,063,680 bytes
# BYTES_PER_AGENT = 12 (dos tensores FP16 de 3 componentes)
# MAX = 8,053,063,680 / 12 = 671,088,640
MAX_AGENTS = 671_088_640

print(f"DEVICE: {device.upper()}")
print(f"MAX TEORICO: {MAX_AGENTS:,} agentes\n")
print(f"{'%':>4} | {'Agentes':>16} | {'VRAM MB':>8} | {'T_min (s)':>12} | {'Agentes/seg':>18} | Estado")
print("-" * 80)

for pct in range(10, 110, 10):
    n  = int(MAX_AGENTS * pct / 100)
    mb = (n * 12) / (1024 ** 2)
    try:
        P = torch.zeros(n, 3, device=device, dtype=dtype)
        V = torch.randn(n, 3, device=device, dtype=dtype) * 0.1

        # warm-up
        _ = P + V
        if device == 'xpu':
            torch.xpu.synchronize()

        # 3 corridas, tomamos el mejor tiempo
        times = []
        for _ in range(3):
            t0 = time.perf_counter()
            R  = P + V
            if device == 'xpu':
                torch.xpu.synchronize()
            times.append(time.perf_counter() - t0)

        best = min(times)
        aps  = n / best

        del P, V, R
        if device == 'xpu':
            torch.xpu.empty_cache()

        print(f"{pct:>4}% | {n:>16,} | {mb:>8.0f} | {best:>12.6f} | {aps:>18,.0f} | OK")

    except Exception:
        print(f"{pct:>4}% | {n:>16,} | {mb:>8.0f} | {'N/A':>12} | {'N/A':>18} | OOM")
