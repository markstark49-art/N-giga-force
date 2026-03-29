import torch
import time
import os
import pandas as pd

# 🛡️ Blindaje Institucional: N-Giga-Forge v20.3
# "Chronos Stable: El Regreso al Origen Exacto"

# === 1. CONFIGURACIÓN DE LABORATORIO ESTABLE ===
DEVICE = "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float32 
NUM_AGENTS = 1048576  
CHUNK_SIZE = 1048576 

print(f"⏳ Iniciando CHRONOS v20.3 (Escala Estable 1M) en {DEVICE.upper()}...")

DT = 0.01 
# Masa Normalizada para evitar la eyección relativista
G_M = 1.0 
G_M_tensor = torch.tensor(G_M, dtype=DTYPE, device=DEVICE)

# --- ASIGNACIÓN DE MEMORIA (100.0x de Radio para Estabilidad) ---
P = torch.randn((NUM_AGENTS, 3), dtype=DTYPE, device=DEVICE) * 100.0 
V = torch.randn((NUM_AGENTS, 3), dtype=DTYPE, device=DEVICE) * 0.1  

acc_buffer = torch.zeros((CHUNK_SIZE, 3), dtype=DTYPE, device=DEVICE)
r_mag_buffer = torch.zeros((CHUNK_SIZE, 1), dtype=DTYPE, device=DEVICE)

# === 2. INTEGRADOR SIMPLÉCTICO (Velocity Verlet) ===
@torch.no_grad()
def compute_acceleration_inplace(pos_chunk, out_acc):
    torch.neg(pos_chunk, out=out_acc)
    torch.sum(out_acc.square(), dim=1, keepdim=True, out=r_mag_buffer)
    r_mag_buffer.add_(1e-6) 
    r_mag_buffer.pow_(-1.5)
    out_acc.mul_(r_mag_buffer).mul_(G_M_tensor)

@torch.no_grad()
def symplectic_step_Verlet():
    compute_acceleration_inplace(P, acc_buffer)
    V.add_(acc_buffer, alpha=DT/2)
    P.add_(V, alpha=DT)
    compute_acceleration_inplace(P, acc_buffer)
    V.add_(acc_buffer, alpha=DT/2)

# === 3. EL PROTOCOLO DE REVERSIÓN Y LA SONDA [0] ===
memoria_sonda = [] 

def run_chronos_con_piloto(steps, label, fase_ida=False):
    print(f"\n--- {label} ({steps} ticks) ---")
    if DEVICE == "xpu": torch.xpu.synchronize()
    elif DEVICE == "cuda": torch.cuda.synchronize()
    start = time.time()
    
    telemetry = []
    
    for step in range(1, steps + 1):
        symplectic_step_Verlet()
        
        # 🎙️ LA SONDA OBSERVA:
        if step % 500 == 0:
            pos_actual = P[0].cpu().clone()
            
            if fase_ida:
                memoria_sonda.append(pos_actual)
                print(f" └─ Sonda [0] grabó el futuro en Tick {step:04d} | Pos Z: {pos_actual[2].item():.5f}")
            else:
                recuerdo = memoria_sonda.pop()
                error_temporal = torch.norm(pos_actual - recuerdo).item()
                print(f" └─ Sonda [0] re-experimentando Tick {steps - step:04d} | Déjà vu Error: {error_temporal:.9f}")
                telemetry.append({"step": step, "error": error_temporal})

    if DEVICE == "xpu": torch.xpu.synchronize()
    elif DEVICE == "cuda": torch.cuda.synchronize()
    print(f"Fase Completada en {time.time() - start:.2f}s")
    return telemetry

if __name__ == "__main__":
    P_origin = P[0].cpu().clone()
    STEPS = 2500

    # 1. FUTURO
    run_chronos_con_piloto(STEPS, "FUTURO (Despliegue de Entropía)", fase_ida=True)

    # 2. EL SALTO
    print("\n💥 LA SONDA [0] ACTIVA LA INVERSIÓN: V = -V ...")
    V.neg_() 

    # 3. PASADO
    telemetry_back = run_chronos_con_piloto(STEPS, "PASADO (Retracción Simpléctica)", fase_ida=False)

    # 4. AUDITORÍA
    P_final = P[0].cpu()
    drift = torch.norm(P_origin - P_final).item()

    print(f"\n🔬 RESULTADO DE LA AUDITORÍA:")
    print(f"Deriva Numérica (FP32 Drift): {drift:.12f}")

    if drift < 1e-3:
        print("🏆 VIAJE EN EL TIEMPO EXITOSO. La Sonda [0] ha regresado al origen exacto.")
    else:
        print("❌ COLAPSO NUMÉRICO.")
        
    # 💾 Telemetría Chronos
    os.makedirs("telemetry_and_proofs", exist_ok=True)
    pd.DataFrame(telemetry_back).to_csv("telemetry_and_proofs/telemetry_chronos_stable_v20.3.csv", index=False)
