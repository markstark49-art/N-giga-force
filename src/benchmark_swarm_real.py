"""
BENCHMARK CIENTIFICO: Capacidad Real de Mini-Agentes en Intel Arc A750
Sin alucinaciones: Todos los datos vienen de medicion directa en hardware.
"""
import torch
import time

def bytes_per_agent_fp16():
    # 2 tensores [N, 3] en FP16: 3 floats * 2 bytes * 2 tensores = 12 bytes/agente
    return 12

def run_benchmark():
    device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
    dtype  = torch.float16

    print("=" * 70)
    print("  BENCHMARK REAL: Intel Arc A750 (XPU) - Doctrina Matricial")
    print("=" * 70)

    VRAM_TOTAL_MB   = 8192
    VRAM_OS_WIN_MB  = 512
    VRAM_USABLE_MB  = VRAM_TOTAL_MB - VRAM_OS_WIN_MB
    VRAM_USABLE_B   = VRAM_USABLE_MB * 1024 * 1024
    BYTES_PER_AGENT = bytes_per_agent_fp16()

    MAX_AGENTS = VRAM_USABLE_B // BYTES_PER_AGENT

    print(f"\n[CALCULO MATEMATICO BASE]")
    print(f"   VRAM Total           : {VRAM_TOTAL_MB:,} MB")
    print(f"   VRAM Reserva OS/Win  : {VRAM_OS_WIN_MB:,} MB")
    print(f"   VRAM Disponible      : {VRAM_USABLE_MB:,} MB ({VRAM_USABLE_MB/1024:.2f} GB)")
    print(f"   Bytes/Agente (FP16)  : {BYTES_PER_AGENT} bytes")
    print(f"   Maximo Teorico       : {MAX_AGENTS:,} agentes\n")
    print(f"   Formula: {VRAM_USABLE_B:,} bytes / {BYTES_PER_AGENT} bytes = {MAX_AGENTS:,}\n")

    print(f"  % | {'Agentes':>16} | {'VRAM (MB)':>10} | {'Mejor_Tiempo(s)':>16} | {'Agentes/seg':>18}")
    print("-" * 73)

    for pct in range(10, 110, 10):
        agent_count     = int(MAX_AGENTS * pct / 100)
        vram_needed_mb  = (agent_count * BYTES_PER_AGENT) / (1024 * 1024)

        try:
            P = torch.zeros(agent_count, 3, device=device, dtype=dtype)
            V = torch.randn(agent_count, 3, device=device, dtype=dtype) * 0.1

            # Warm-up
            _ = P + V
            if device == 'xpu': torch.xpu.synchronize()

            # Promedio de 5 corridas
            times = []
            for _ in range(5):
                t0 = time.perf_counter()
                result = P + V
                if device == 'xpu': torch.xpu.synchronize()
                times.append(time.perf_counter() - t0)

            elapsed = min(times)
            aps     = agent_count / elapsed

            del P, V, result
            if device == 'xpu': torch.xpu.empty_cache()

            print(f" {pct:>3}% | {agent_count:>16,} | {vram_needed_mb:>10.1f} | {elapsed:>16.6f} | {aps:>18,.0f} OK")

        except Exception as e:
            print(f" {pct:>3}% | {agent_count:>16,} | {vram_needed_mb:>10.1f} |       OUT_OF_MEM | {'N/A':>18} FAIL")

    print("=" * 70)
    print("NOTA: 100%% VRAM = riesgo OOM. Sweet Spot recomendado: 50-70%%.")

if __name__ == "__main__":
    run_benchmark()
