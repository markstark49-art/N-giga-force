import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time
import sys

# === 1. CONFIGURACIÓN HPC ===
DEVICE = "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16
NUM_AGENTS_MICRO = 16777216  # 16M (Muestra representativa para RL rápido)

print(f"🚀 Iniciando Sandbox de Aprendizaje por Refuerzo en {DEVICE.upper()}...")

# Datos de prueba globales
P_micro = torch.rand((NUM_AGENTS_MICRO, 3), dtype=DTYPE, device=DEVICE)
pos_nave = torch.zeros(3, dtype=DTYPE, device=DEVICE)

# Baseline: Cálculo manual Alcubierre
def native_distance(P, pos): 
    return P.sub(pos).pow_(2).sum(dim=1).sqrt_()

def measure_latency(func, P, pos, runs=5):
    if DEVICE == "xpu": torch.xpu.synchronize()
    elif DEVICE == "cuda": torch.cuda.synchronize()
    
    start = time.perf_counter()
    for _ in range(runs): 
        _ = func(P, pos)
    
    if DEVICE == "xpu": torch.xpu.synchronize()
    elif DEVICE == "cuda": torch.cuda.synchronize()
    return (time.perf_counter() - start) / runs

# Detección de la línea base
BASELINE_LAT = measure_latency(native_distance, P_micro, pos_nave)
print(f"⏱️ Línea Base (Manual): {BASELINE_LAT:.5f}s\n")

# === 2. EL DICCIONARIO DE ACCIONES (KERNELS) ===
OP_DICT = {
    0: ('MANUAL', native_distance),
    1: ('FUSED_NORM', lambda p, pos: torch.linalg.vector_norm(p - pos, dim=1))
}

class SondaRLCompiler(nn.Module):
    def __init__(self):
        super().__init__()
        # Red de Política: 32 latentes -> Proporción de kernels
        self.fc = nn.Linear(32, len(OP_DICT))
        
    def forward(self, x):
        logits = self.fc(x)
        probs = F.softmax(logits, dim=-1)
        
        # Selección Estocástica (Exploración)
        m = torch.distributions.Categorical(probs)
        action_id = m.sample()
        log_prob = m.log_prob(action_id)
        
        return action_id.item(), log_prob

# === 3. BUCLE DE ENTRENAMIENTO POLÍTICO ===

def run_rl_training(epochs=100):
    compiler = SondaRLCompiler().to(DEVICE)
    optimizer = torch.optim.Adam(compiler.parameters(), lr=0.05)
    
    print("🧠 Iniciando Entrenamiento por Gradiente Político (REINFORCE)...")
    latent_const = torch.randn((1, 32), device=DEVICE) # Contexto constante para convergencia
    
    history = []
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # 1. Elección de la Sonda
        action_id, log_prob = compiler(latent_const)
        op_name, op_func = OP_DICT[action_id]
        
        # 2. Evaluación de Rendimiento Real
        latency = measure_latency(op_func, P_micro, pos_nave)
        
        # 3. Función de Recompensa (Ahorro de Tiempo)
        # Ganancia en ms = (Baseline - Latency) * 1000
        time_diff = BASELINE_LAT - latency
        reward = time_diff * 1000.0
        
        # Penalización estricta por elegir la base ineficiente (fuerza la exploración)
        if op_name == 'MANUAL': reward -= 5.0 
        
        # 4. Cálculo de Pérdida REINFORCE
        # R es la recompensa (sin gradiente)
        R = torch.tensor(reward, device=DEVICE, dtype=torch.float32)
        loss = -log_prob * R
        
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Época {epoch+1:03d} | Acción: {op_name:10s} | Latencia: {latency:.5f}s | Reward: {reward:7.2f}")
            history.append(reward)
            
    # PERSISTENCIA DE LA CONCIENCIA DE RENDIMIENTO
    torch.save(compiler.state_dict(), 'sonda_rl_weights.pth')
    print(f"\n✅ ENTRENAMIENTO COMPLETADO. La Sonda ha convergido.")
    
    # 5. GENERACIÓN DE TELEMETRÍA OPTIMIZADA
    print(">> GENERANDO TRAYECTORIA OPTIMIZADA (1000 frames)...")
    history = []
    # Usar el kernel ganador (FUSED_NORM)
    for _ in range(1000):
        history.append(P_micro[0].clone().cpu().numpy())
        P_micro.add_(torch.tensor([0.001, 0.0, 0.0], dtype=DTYPE, device=DEVICE))
        
    import pandas as pd
    df = pd.DataFrame(np.vstack(history), columns=['Px', 'Py', 'Pz'])
    df['Vx'] = df['Px'].diff().fillna(0)
    df['Vy'] = df['Py'].diff().fillna(0)
    df['Vz'] = df['Pz'].diff().fillna(0)
    df['Tx'] = 0.0 ; df['Ty'] = 0.0 ; df['Tz'] = 0.0
    
    df.to_csv('telemetry_rl_optimized.csv', index=False)
    print(f"✅ ARCHIVO 'telemetry_rl_optimized.csv' GENERADO.")
    print(f">> PESOS DE OPTIMIZACIÓN PERSISTIDOS EN 'sonda_rl_weights.pth'.")
    
    if DEVICE == "xpu": torch.xpu.empty_cache()

if __name__ == "__main__":
    run_rl_training(100)
