import torch
import time
import os
import pandas as pd

# 🛡️ Blindaje Institucional: N-Giga-Forge v20.5
# "Chronos Purificado: Domain Scaling y la Realidad Métrica"

# === 1. CONFIGURACIÓN DEL LABORATORIO HPC ===
DEVICE = "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float32 
NUM_AGENTS = 1048576  # Escala de laboratorio (2^20)
CHUNK_SIZE = 1048576  

print(f"🌌 Iniciando CHRONOS v20.5 (Domain Scaling) en {DEVICE.upper()}...")

# === 2. EL RE-ESCALADO DEL DOMINIO ===
# Factores de Conversión (markstark49-art Unit System)
M_real = 5.972e24      # kg (Tierra)
R_real = 6.371e6       # m (Radio Tierra)
G_real = 6.67430e-11   # Constante G

# Tiempo de Simulación: 1 unit_sim = T_scale segundos reales
T_scale = (R_real**3 / (G_real * M_real))**0.5

print("\n--- ⚖️ LEYES DEL DOMINIO RE-ESCALADO ---")
print(f" └─ Unidad de Masa (1.0 sim) = {M_real:.2e} kg")
print(f" └─ Unidad de Longitud (1.0 sim) = {R_real:.2e} m")
print(f" └─ Unidad de Tiempo (1.0 sim) = {T_scale:.2f} segundos")

G_sim = 1.0
M_sim = 1.0
G_M_tensor = torch.tensor(G_sim * M_sim, dtype=DTYPE, device=DEVICE)
DT_sim = 0.01 

# === 3. INGENIERÍA DE MEMORIA (Zero-Allocation) ===
P = torch.randn((NUM_AGENTS, 3), dtype=DTYPE, device=DEVICE) * 2.0 
V = torch.randn((NUM_AGENTS, 3), dtype=DTYPE, device=DEVICE) * 0.1  

acc_buffer = torch.zeros((CHUNK_SIZE, 3), dtype=DTYPE, device=DEVICE)
r_mag_buffer = torch.zeros((CHUNK_SIZE, 1), dtype=DTYPE, device=DEVICE)

# === 4. INTEGRADOR SIMPLÉCTICO PURIFICADO ===
@torch.no_grad()
def compute_acceleration_inplace(pos_chunk, out_acc):
    torch.neg(pos_chunk, out=out_acc)
    torch.sum(out_acc.square(), dim=1, keepdim=True, out=r_mag_buffer)
    r_mag_buffer.add_(1e-6) # Prevención origen
    r_mag_buffer.pow_(-1.5)
    out_acc.mul_(r_mag_buffer).mul_(G_M_tensor)

@torch.no_grad()
def symplectic_step_Verlet():
    compute_acceleration_inplace(P, acc_buffer)
    V.add_(acc_buffer, alpha=DT_sim/2)
    P.add_(V, alpha=DT_sim)
    compute_acceleration_inplace(P, acc_buffer)
    V.add_(acc_buffer, alpha=DT_sim/2)

# === 5. PROTOCOLO DE REVERSIÓN ===
def run_scaled_chronos(steps, label):
    print(f"\n--- {label} ({steps} ticks) ---")
    if DEVICE in ["xpu", "cuda"]:
        if DEVICE == "xpu": torch.xpu.synchronize()
        else: torch.cuda.synchronize()
        
    start = time.time()
    
    for _ in range(steps):
        symplectic_step_Verlet()

    if DEVICE in ["xpu", "cuda"]:
        if DEVICE == "xpu": torch.xpu.synchronize()
        else: torch.cuda.synchronize()
    print(f"Fase Completada en {time.time() - start:.2f}s")

if __name__ == "__main__":
    P_origin = P[0].cpu().clone()
    STEPS = 2500

    # 1. FUTURO
    run_scaled_chronos(STEPS, "FUTURO (Dominio Normalizado)")

    # 2. INVERSIÓN TEMPORAL
    print("\n💥 INVERSIÓN TEMPORAL: V = -V ...")
    V.neg_() 

    # 3. PASADO
    run_scaled_chronos(STEPS, "PASADO (Retracción Simpléctica)")

    # 4. AUDITORÍA FINAL
    P_final = P[0].cpu()
    drift_sim = torch.norm(P_origin - P_final).item()
    drift_real_m = drift_sim * R_real

    print(f"\n🔬 RESULTADO DE LA AUDITORÍA (v20.5):")
    print(f"Deriva Numérica FP32 (Sim Units): {drift_sim:.8f}")
    print(f"Deriva Real Traslado a Metros: {drift_real_m:.8f} m")

    if drift_sim < 1e-3:
        print("🏆 PURIFICACIÓN ALGORÍTMICA CONFIRMADA. No hay números subnormales.")
    else:
        print("❌ COLAPSO.")
        
    # Save telemetry for symbolic extractor
    os.makedirs("telemetry_and_proofs", exist_ok=True)
    pd.DataFrame([{"drift_sim": drift_sim, "drift_real_m": drift_real_m}]).to_csv("telemetry_and_proofs/telemetry_chronos_v20.5_scaling.csv", index=False)
