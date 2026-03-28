import torch
import time
import csv
import sys

device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
dtype  = torch.float16
MAX_AGENTS = 671_088_640  # (8192-512)*1024*1024 / 12

rows = []
for pct in range(10, 110, 10):
    n   = int(MAX_AGENTS * pct / 100)
    mb  = round((n * 12) / (1024**2), 1)
    try:
        P = torch.zeros(n, 3, device=device, dtype=dtype)
        V = torch.randn(n, 3, device=device, dtype=dtype) * 0.1
        _ = P + V
        if device == 'xpu': torch.xpu.synchronize()
        times = []
        for _ in range(3):
            t0 = time.perf_counter()
            R  = P + V
            if device == 'xpu': torch.xpu.synchronize()
            times.append(time.perf_counter() - t0)
        best = min(times)
        aps  = int(n / best)
        del P, V, R
        if device == 'xpu': torch.xpu.empty_cache()
        rows.append([pct, n, mb, round(best, 6), aps, 'OK'])
    except Exception:
        rows.append([pct, n, mb, 'N/A', 'N/A', 'OOM'])

with open('bench_results.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['pct', 'agentes', 'vram_mb', 't_min_s', 'agentes_per_sec', 'status'])
    w.writerows(rows)

print("CSV GUARDADO")
for r in rows:
    print(','.join(str(x) for x in r))
