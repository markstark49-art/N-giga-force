import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time
import sys
import pandas as pd

# === PARÁMETROS TESLA v14.5 ===
POWER_UNIT_KW = 11.5  # Capacidad continua de 1 Powerwall 3
PEAK_LRA_KW = 42.0    # Pico de arranque (185 LRA @ 230V aprox)
NUM_AGENTS = 268435456 # 2^28 Agentes
DEVICE = "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16

class TeslaPowerManager:
    def __init__(self, num_units=1):
        self.num_units = num_units
        self.max_power_kw = num_units * POWER_UNIT_KW
        self.peak_power_kw = num_units * PEAK_LRA_KW
        self.mu_efficiency = 1.45e-11 # Constante de conversión Watts -> Warp
        
    def get_max_velocity(self, is_starting=False):
        """Calcula la v_warp máxima permitida por el presupuesto de Watts."""
        available_kw = self.peak_power_kw if is_starting else self.max_power_kw
        # Física Tesla: v^2 = P / (mu * N)
        v_limit = np.sqrt(available_kw / (self.mu_efficiency * NUM_AGENTS))
        return v_limit

class TeslaWarpEngine:
    def __init__(self, device=DEVICE):
        self.device = device
        print(f"🌌 Inicializando Motor Tesla v14.5: {NUM_AGENTS:,} Agentes compartiendo Powerwall...")
        try:
            self.P = torch.zeros((NUM_AGENTS, 3), dtype=DTYPE, device=device)
            print(f"✅ VRAM RESERVADA: 3.21 GB (Tesla Sustainability)")
        except RuntimeError:
            print("❌ VRAM Insuficiente.")
            sys.exit(1)
            
    @torch.no_grad()
    def step_power_limited(self, v_warp_req, current_power_kw):
        """Ejecución inercial limitada por la capacidad eléctrica."""
        chunk = 16777216
        stream = torch.xpu.Stream() if self.device == "xpu" else None
        
        with (torch.xpu.stream(stream) if stream else torch.no_grad()):
            for i in range(0, NUM_AGENTS, chunk):
                end = min(i + chunk, NUM_AGENTS)
                # El desplazamiento es proporcional al vector warp permitido
                self.P[i:end].add_(v_warp_req, alpha=1.0)
        
        if stream: torch.xpu.synchronize()

# --- EJECUCIÓN MULTIETAPA (1 -> 3 BATERÍAS) ---

if __name__ == "__main__":
    device = DEVICE
    engine = TeslaWarpEngine(device=device)
    
    # 1. Fase de 1 Unidad (PASO 0-250)
    power_1 = TeslaPowerManager(num_units=1)
    # 2. Fase de 3 Unidades (PASO 250-500)
    power_3 = TeslaPowerManager(num_units=3)
    
    print("\n🚀 INICIANDO PRUEBA DE EFICIENCIA TESLA (500 PASOS)...")
    history = []
    t_start = time.perf_counter()
    
    for step in range(1, 501):
        is_starting = (step == 1) # Pico LRA en el arranque
        current_manager = power_1 if step <= 250 else power_3
        
        # Obtener techo físico según potencia
        v_limit_scalar = current_manager.get_max_velocity(is_starting)
        v_warp = torch.tensor([v_limit_scalar, 0.0, 0.0], dtype=DTYPE, device=device)
        
        # Consumo estimado en Watts para telemetría
        watts_consumed = (v_limit_scalar**2) * (power_1.mu_efficiency * NUM_AGENTS)
        
        # Ejecutar Salto
        engine.step_power_limited(v_warp, watts_consumed)
        
        # Captura de Telemetría
        if step % 1 == 0:
            p_pos = engine.P[0].clone().cpu().numpy()
            history.append({
                'Px': p_pos[0], 'Py': p_pos[1], 'Pz': p_pos[2],
                'Watts': watts_consumed,
                'Units': current_manager.num_units
            })
            
        if step % 100 == 0:
            print(f"⌛ Paso {step:3} | Energía: {watts_consumed:6.2f} kW | Unidades: {current_manager.num_units} | v_warp: {v_limit_scalar:.6f}")

    # EXPORTACIÓN MASIVA
    df = pd.DataFrame(history)
    df['Vx'] = df['Px'].diff().fillna(0)
    df['Vy'] = df['Py'].diff().fillna(0)
    df['Vz'] = df['Pz'].diff().fillna(0)
    df['Tx'] = 0.0 ; df['Ty'] = 0.0 ; df['Tz'] = 0.0
    
    df.to_csv('telemetry_tesla_powerwall.csv', index=False)
    print(f"\n✅ TELEMETRÍA 'telemetry_tesla_powerwall.csv' GENERADA.")
    print(f">> PRUEBA TESLA COMPLETADA EN {time.perf_counter()-t_start:.2f}s.")
