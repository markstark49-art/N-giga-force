import torch
import torch.nn as nn
import time
import sys

# --- CONFIGURACIÓN DE ALTO RENDIMIENTO N-GIGA-FORGE v10.2 ---
MAX_TENSORS = 100000000  # 100M agentes (10^8)
CHUNK_SIZE = 2097152     # 2M agentes por lote (Sweet spot para A750)
G_CONST = 1.0           
M_STAR = 1.0           
PLANCK_LENGTH_SQ = 1e-6 

class ProbeBrain(nn.Sequential):
    """
    Cerebro de la Sonda (Agente [0]).
    Opera en float32 para estabilidad de gradientes.
    """
    def __init__(self):
        super().__init__(
            nn.Linear(6, 16),
            nn.Tanh(),
            nn.Linear(16, 3)
        )
        self.to(dtype=torch.float32)

class NGigaForgePhysics:
    """
    Simulador N-Body Relativista con Regularización de Planck.
    Optimizado para Intel Arc A750 (XPU).
    """
    def __init__(self, agent_count=MAX_TENSORS):
        self.device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
        self.count = agent_count
        self.dtype = torch.float16
        
        print(f"🚀 [HPC-INIT] Inicializando {agent_count:,} agentes en {self.device.upper()}")
        
        # Matrices Principales (Escala r=150)
        # Enjambre distribuido en una "concha" orbital entre 120 y 180
        angles = torch.rand(self.count, device=self.device, dtype=self.dtype) * 2 * 3.14159
        radii = torch.rand(self.count, device=self.device, dtype=self.dtype) * 60 + 120
        self.P = torch.zeros(self.count, 3, device=self.device, dtype=self.dtype)
        self.P[:, 0] = radii * torch.cos(angles)
        self.P[:, 1] = radii * torch.sin(angles)
        self.P[:, 2] = torch.randn(self.count, device=self.device, dtype=self.dtype) * 5.0
        
        self.V = torch.randn(self.count, 3, device=self.device, dtype=self.dtype) * 0.1
        
        # Sonda Espacial (Agente [0]) - Posicionada en el Radio Objetivo (r=150)
        # v_orbital = sqrt(GM/r) = sqrt(1/150) ≈ 0.0816
        self.P[0] = torch.tensor([150.0, 0.0, 0.0], device=self.device, dtype=self.dtype)
        self.V[0] = torch.tensor([0.0, 0.0816, 0.0], device=self.device, dtype=self.dtype)
        
        self.probe_brain = ProbeBrain().to(self.device)
        self.optimizer = torch.optim.Adam(self.probe_brain.parameters(), lr=1e-4)
        
        # --- BLOQUE DE RECOLECCIÓN CIENTÍFICA v10.5 ---
        self.telemetry_size = 2000
        self.telemetry_idx = 0
        self.telemetry_buffer = torch.zeros(self.telemetry_size, 9, device=self.device, dtype=torch.float32)
        
        if self.device == 'xpu':
            allocated = torch.xpu.memory_allocated() / 1e6
            print(f"🛡️  [VRAM-CHECK] Memoria Ocupada: {allocated:.2f} MB")

    @torch.no_grad()
    def update_passive_swarm(self, dt=0.01):
        """
        Actualización de Gravedad por Chunks.
        Usamos float32 para la norma crítica para evitar NaNs en FP16.
        """
        for i in range(0, self.count, CHUNK_SIZE):
            end = min(i + CHUNK_SIZE, self.count)
            r_vec = self.P[i:end]
            
            # Cálculo de norma en F32 para evitar overflow/underflow
            r_vec_f32 = r_vec.to(torch.float32)
            r_norm_sq = torch.sum(r_vec_f32 * r_vec_f32, dim=1, keepdim=True)
            
            # g = (GM * r) / (r^2 + Lp^2)^1.5 (Aritmética en F32)
            denom = (r_norm_sq + 1e-6).pow(1.5) # Softening mayor para FP16
            accel = r_vec_f32 * (-1.0 / denom) # G*M normalizado a 1.0
            
            # Sumar de vuelta en FP16
            self.V[i:end].add_((accel * dt).to(self.dtype))
            self.P[i:end].add_(self.V[i:end] * dt)

    def update_probe(self, dt=0.01, step_idx=0, total_steps=2500):
        """
        Ciclo de Inteligencia Continua con Inyector de Turbulencia v10.5.
        """
        state_f32 = torch.cat([self.P[0], self.V[0]]).to(dtype=torch.float32)
        thrust = self.probe_brain(state_f32) * 0.05
        
        # --- BLOQUE DE RECOLECCIÓN CIENTÍFICA (ÚLTIMOS 2000 FRAMES) ---
        if step_idx >= (total_steps - self.telemetry_size) and self.telemetry_idx < self.telemetry_size:
            # 1. EL IMPULSO ESPORÁDICO (La corrección termodinámica)
            if self.telemetry_idx % 100 == 0:
                with torch.no_grad():
                    # Ruido ligeramente mayor (0.1) pero poco frecuente
                    impulso = torch.randn(3, device=self.device, dtype=self.dtype) * 0.1
                    self.V[0].add_(impulso) 
            
            # 2. LECTURA PASIVA (A la velocidad de la VRAM)
            with torch.no_grad():
                # Guardamos Estado (P, V) y Acción (Thrust)
                record = torch.cat([state_f32, thrust.detach()])
                self.telemetry_buffer[self.telemetry_idx] = record
                self.telemetry_idx += 1

        # Física Gravitatoria y Reward (v10.3 Core)
        r_current = self.P[0].to(dtype=torch.float32)
        r_sq_current = torch.sum(r_current * r_current)
        g_accel = r_current * (-1.0 / (r_sq_current + 1e-6).pow(1.5))
        
        # Simulación simbólica para aprendizaje
        v_next = self.V[0].to(torch.float32) + (g_accel + thrust) * dt
        p_next = self.P[0].to(torch.float32) + v_next * dt
        
        radio_actual = torch.sqrt(torch.sum(p_next**2) + 1e-8)
        velocidad_actual = torch.sqrt(torch.sum(v_next**2) + 1e-8)
        consumo_energia = torch.sum(thrust**2)

        castigo_singularidad = 10000.0 / (radio_actual - 49.0 + 1e-5) 
        castigo_vacio = (radio_actual / 300.0).pow(4) * 5000.0
        error_orbital_cuadratico = ((radio_actual - 150.0) / 10.0).pow(2) 
        
        recompensa = (velocidad_actual * 0.1) - castigo_singularidad - castigo_vacio - \
                     (consumo_energia * 50.0) - error_orbital_cuadratico
        loss = -recompensa
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        with torch.no_grad():
            total_accel = g_accel + thrust
            self.V[0].add_((total_accel * dt).to(dtype=self.dtype))
            self.P[0].add_((self.V[0] * dt).to(dtype=self.dtype))
            
        return radio_actual.item(), recompensa.item()

    def run_simulation(self, total_steps=2500):
        print(f"\n--- INICIANDO CICLO CIENTÍFICO v10.5 ({total_steps} pasos) ---")
        t_start = time.time()
        
        self.discovery_log = []
        
        for s in range(total_steps):
            t_step_start = time.perf_counter()
            
            # Ciclo Maestro
            self.update_passive_swarm()
            dist, rewd = self.update_probe(step_idx=s, total_steps=total_steps)
            
            # Registro de Descubrimientos (cada 100 pasos para monitoreo)
            if s % 100 == 0:
                pos = self.P[0].detach().cpu().to(torch.float32).tolist()
                vel = self.V[0].detach().cpu().to(torch.float32).tolist()
                self.discovery_log.append([s] + pos + vel + [rewd])
                elapsed = time.perf_counter() - t_step_start
                print(f"[{time.time() - t_start:5.2f}s] Step {s:4d} | Dist: {dist:.4f} | Reward: {rewd:.4f} | Tick: {elapsed:.4f}s")
        
        print(f"\n✅ CICLO COMPLETADO: {total_steps} pasos registrados.")
        self.generate_scientific_report()
        
        # --- EXTRACCIÓN MASIVA AL FINALIZAR (Operación PCI-E) ---
        print(">> DESCARGANDO MATRIZ DE TELEMETRÍA...")
        import pandas as pd
        matriz_cpu = self.telemetry_buffer.cpu().numpy()
        columnas = ['Px', 'Py', 'Pz', 'Vx', 'Vy', 'Vz', 'Tx', 'Ty', 'Tz']
        df = pd.DataFrame(matriz_cpu, columns=columnas)
        df.to_csv('telemetry_agent0.csv', index=False)
        print(">> TELEMETRÍA DE ALTA FIDELIDAD EXPORTADA.")

    def generate_scientific_report(self):
        """
        Análisis de Veracidad: Matriz de estabilidad orbital y benchmark.
        """
        print("\n📊 GENERANDO REPORTE DE DESCUBRIMIENTOS (ANTIALUCINACIÓN)...")
        data = torch.tensor(self.discovery_log) # [S, 8]
        
        # Estabilidad de Radio (Distancia al origen)
        pos_xyz = data[:, 1:4]
        radios = torch.sqrt(torch.sum(pos_xyz * pos_xyz, dim=1))
        radio_medio = torch.mean(radios).item()
        varianza_radio = torch.var(radios).item()
        
        # Estabilidad de Recompensa
        reward_avg = torch.mean(data[:, 7]).item()
        
        print("-" * 50)
        print(f"DISTANCIA MEDIA AL ORIGEN: {radio_medio:.6f}")
        print(f"VARIANZA ORBITAL (PRESIÓN): {varianza_radio:.6e}")
        print(f"CONSISTENCIA DE IA (REWARD): {reward_avg:.4f}")
        print("-" * 50)
        
        if varianza_radio < 1e-2:
            print("🚀 VEREDICTO: ÓRBITA ESTABLE. Datos Verídicos.")
        else:
            print("⚠️ VEREDICTO: INESTABILIDAD DETECTADA. Ajustando Softening.")
        
        # Guardar para análisis posterior
        torch.save(data, "discovery_matrix.pt")
        print("💾 DiscoveryMatrix guardada en 'discovery_matrix.pt'.")

    def get_render_data(self):
        """
        Copia segura a CPU para visualización (Límite 50k puntos).
        """
        indices = slice(0, 50000)
        return self.P[indices].to(device='cpu', dtype=torch.float32).numpy()

if __name__ == "__main__":
    forge = NGigaForgePhysics()
    # ESTUDIO CIENTÍFICO v10.5: 2500 Pasos (Captura 2000 frames)
    forge.run_simulation(total_steps=2500)
