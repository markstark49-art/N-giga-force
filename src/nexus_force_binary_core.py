import torch
import torch.nn as nn
import numpy as np
import time
import pandas as pd

# CONFIGURACIÓN HPC v11.0 (Arc A750)
MAX_TENSORS = 100000000  # 100M Agentes
CHUNK_SIZE = 67108864    # 64M GPU Aligned
L_P_SQ = 1e-6            # Planck Regularization (Lp^2)
M_A = 1.0                # Masa Sol A
M_B = 1.0                # Masa Sol B
R_STAR = 75.0            # Radio orbital de las estrellas
OMEGA = 0.02             # Velocidad angular orbital

class ResidualBrain(nn.Module):
    """
    PINN (Physics-Informed Neural Network).
    Divide la lógica en Instinto (PySR) vs Residuo (MLP).
    """
    def __init__(self):
        super().__init__()
        # EL RESIDUO: Maneja el caos y correcciones Figure-8
        self.mlp = nn.Sequential(
            nn.Linear(6, 64),
            nn.Tanh(),
            nn.Linear(64, 64),
            nn.Tanh(),
            nn.Linear(64, 3)
        )
        # K-PySR: Constante extraída de la fase v10.5
        self.register_buffer('k_pysr', torch.tensor(1.65e-4))

    def get_instinct(self, p_agent, p_star):
        """
        Teorema PySR v10.5: Inverso del Cuadrado Vectorizado.
        """
        r_rel = p_agent - p_star
        r_sq = torch.sum(r_rel**2) + L_P_SQ
        # Ley de Potencia: Empuje compensatorio hacia el radio de equilibrio
        thrust = -r_rel * (self.k_pysr / (r_sq.pow(1.5))) 
        return thrust

    def forward(self, p_agent, v_agent, p_starA, p_starB):
        # 1. EL INSTINTO (Superposición de PySR)
        instinct_A = self.get_instinct(p_agent, p_starA)
        instinct_B = self.get_instinct(p_agent, p_starB)
        instinct_total = instinct_A + instinct_B
        
        # 2. EL RESIDUO (Corrección de Caos)
        # El MLP evalúa el estado completo relativo al centro de masas
        state = torch.cat([p_agent, v_agent])
        mlp_out = self.mlp(state) * 0.02 # Escala baja para forzar física pura
        
        return instinct_total + mlp_out, mlp_out

class NGigaForgeBinary:
    def __init__(self, agent_count=100_000_000):
        self.device = 'xpu' if torch.xpu.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'
        self.dtype = torch.float16
        self.count = agent_count
        self.t = 0.0 # Reloj Maestro
        
        print(f"🚀 [HPC-INIT] v11.0 SISTEMA BINARIO: {agent_count:,} agentes en {self.device.upper()}")
        
        # Posiciones y Velocidades del Enjambre (Escala r=150)
        angles = torch.rand(self.count, device=self.device, dtype=self.dtype) * 2 * 3.14159
        radii = torch.rand(self.count, device=self.device, dtype=self.dtype) * 100 + 100
        self.P = torch.zeros(self.count, 3, device=self.device, dtype=self.dtype)
        self.P[:, 0] = radii * torch.cos(angles)
        self.P[:, 1] = radii * torch.sin(angles)
        self.P[:, 2] = torch.randn(self.count, device=self.device, dtype=self.dtype) * 10.0
        self.V = torch.randn(self.count, 3, device=self.device, dtype=self.dtype) * 0.05
        
        # Sonda Espacial (Agente [0]) - Iniciada en el ecuador binario
        self.P[0] = torch.tensor([150.0, 0.0, 0.0], device=self.device, dtype=self.dtype)
        self.V[0] = torch.tensor([0.0, 0.08, 0.0], device=self.device, dtype=self.dtype)
        
        self.brain = ResidualBrain().to(self.device)
        self.optimizer = torch.optim.Adam(self.brain.parameters(), lr=1e-4)
        
        # Buffer de Telemetría v11.0 (2,000 frames)
        self.telemetry_size = 2000
        self.telemetry_idx = 0
        self.telemetry_buffer = torch.zeros(self.telemetry_size, 9, device=self.device, dtype=torch.float32)

    def get_star_positions(self):
        """
        Dinámica Binaria Inmutable.
        """
        p_a = torch.tensor([R_STAR * np.cos(OMEGA * self.t), R_STAR * np.sin(OMEGA * self.t), 0.0], device=self.device, dtype=torch.float32)
        p_b = -p_a # Simetría perfecta respecto al Baricentro [0,0,0]
        return p_a, p_b

    def update_passive_swarm(self, dt=0.01):
        p_a, p_b = self.get_star_positions()
        
        for i in range(1, self.count, CHUNK_SIZE):
            end = min(i + CHUNK_SIZE, self.count)
            p_chunk = self.P[i:end].to(torch.float32)
            
            # Superposición Gravitatoria: g = g_A + g_B
            r_rel_a = p_chunk - p_a
            r_sq_a = torch.sum(r_rel_a**2, dim=1, keepdim=True) + L_P_SQ
            g_a = r_rel_a * (-M_A / (r_sq_a.pow(1.5)))
            
            r_rel_b = p_chunk - p_b
            r_sq_b = torch.sum(r_rel_b**2, dim=1, keepdim=True) + L_P_SQ
            g_b = r_rel_b * (-M_B / (r_sq_b.pow(1.5)))
            
            total_accel = g_a + g_b
            self.V[i:end].add_((total_accel * dt).to(self.dtype))
            self.P[i:end].add_(self.V[i:end] * dt)

    @torch.no_grad()
    def soliton_warp_step(self, warp_displacement_vector, freq_duty_cycle=0.5):
        """
        Simulación de Solitones de Lentz v13.0 (Low Energy)
        Física de pulsos: $f(r) = \exp(-|r-R|/w)$
        """
        R = 50.0       # Radio del solitón
        width = 12.0   # Grosor de la onda de Lentz (Damping factor)
        
        # 1. El Baricentro de la Pulsación
        pos_nave = self.P[0].clone().to(torch.float32) 
        # Modulación PWM (V12 Mapping): Solo aplicamos el desplazamiento en el 'duty cycle'
        v_warp = (warp_displacement_vector.to(torch.float32)) * freq_duty_cycle
        
        # 2. Mover el Tejido con Solitones (100M Agentes)
        for i in range(1, self.count, CHUNK_SIZE):
            end_idx = min(i + CHUNK_SIZE, self.count)
            r_vec = self.P[i:end_idx].to(torch.float32) - pos_nave
            r_mag = torch.sqrt(torch.sum(r_vec**2, dim=1, keepdim=True) + 1e-8)
            
            # Perfil de Solitón Exponencial (Energía Positiva/Equilibrada)
            # Mucho más eficiente que la pared de Tanh
            f_r = torch.exp(-torch.abs(r_mag - R) / width)
            
            # Desplazamiento del tejido
            self.P[i:end_idx].add_((f_r * v_warp).to(self.dtype))
            
            # --- REDUCCIÓN DE HAWKING (90% menos de estrés térmico) ---
            # Al ser un pulso, la inyección es mínima (0.005 vs 0.05 anterior)
            ruido_termico = (f_r * v_warp) * 0.005 
            self.V[i:end_idx].add_(ruido_termico.to(self.dtype))
            
            del r_vec, r_mag, f_r, ruido_termico
            
        # 3. Resolución de la Paradoja del Ancla
        self.P[0].add_(v_warp.to(self.dtype))

    def update_probe(self, dt=0.01, step_idx=0, total_steps=2500):
        p_a, p_b = self.get_star_positions()
        
        p_0 = self.P[0].to(torch.float32)
        v_0 = self.V[0].to(torch.float32)
        
        # Brain Predictivo (PINN)
        thrust, mlp_out = self.brain(p_0, v_0, p_a, p_b)
        
        # --- ACTIVACIÓN DE SOLITONES v13.0 (Low Energy) ---
        # Sincronizamos la pulsación con el vector residual del cerebro PINN.
        mlp_mag = torch.sqrt(torch.sum(mlp_out**2))
        warp_active = mlp_mag > 0.01
        if warp_active:
            # V12 Mapping: Pulsa cada frame con un ciclo del 100% solo
            # si el caos es inmanejable. Para v13.0 usamos duty_cycle de 0.8
            self.soliton_warp_step(mlp_out * dt * 50.0, freq_duty_cycle=0.8)
        
        # Física Predictiva (v11.0)
        # Superposición g_A + g_B
        r_rel_a = p_0 - p_a
        r_sq_a = torch.sum(r_rel_a**2) + L_P_SQ
        g_a = r_rel_a * (-M_A / (r_sq_a.pow(1.5)))
        
        r_rel_b = p_0 - p_b
        r_sq_b = torch.sum(r_rel_b**2) + L_P_SQ
        g_b = r_rel_b * (-M_B / (r_sq_b.pow(1.5)))
        
        g_total = g_a + g_b
        
        v_next = v_0 + (g_total + thrust) * dt
        p_next = p_0 + v_next * dt
        
        # INGENIERÍA DE RECOMPENSAS (Caos Binario)
        dist_a = torch.sqrt(torch.sum((p_next - p_a)**2) + 1e-8)
        dist_b = torch.sqrt(torch.sum((p_next - p_b)**2) + 1e-8)
        velocidad_sq = torch.sum(v_next**2)
        residue_penalty = torch.sum(mlp_out**2) * 100.0 # Penalización severa al residuo
        
        # Barreras Asintóticas (Planck Singularity)
        r_critico = 30.0
        punish_a = 5000.0 / (dist_a - r_critico + 1e-5)
        punish_b = 5000.0 / (dist_b - r_critico + 1e-5)
        # Castigo por escape (Vacío)
        r_current = torch.sqrt(torch.sum(p_next**2))
        punish_vacio = (r_current / 400.0).pow(4) * 10000.0
        
        # Reward: Velocidad (Energía) - Singularidades - Residuo - Vacío
        # Queremos Figure-8: Mucha velocidad, muy poca dependencia del MLP.
        recompensa = (velocidad_sq * 10.0) - punish_a - punish_b - residue_penalty - punish_vacio
        
        loss = -recompensa
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        with torch.no_grad():
            self.V[0].add_(((g_total + thrust) * dt).to(self.dtype))
            self.P[0].add_((self.V[0] * dt).to(dtype=self.dtype))
            
            # Telemetría Científica (v11.0 Bridge)
            if step_idx >= (total_steps - self.telemetry_size) and self.telemetry_idx < self.telemetry_size:
                record = torch.cat([p_0, v_0, thrust.detach()])
                self.telemetry_buffer[self.telemetry_idx] = record
                self.telemetry_idx += 1
                
        self.t += dt
        return r_current.item(), recompensa.item()

    def run_simulation(self, total_steps=2500):
        print(f"\n--- INICIANDO CICLO BINARIO v11.0 ({total_steps} pasos) ---")
        t_start = time.time()
        for s in range(total_steps):
            t_step_start = time.perf_counter()
            self.update_passive_swarm()
            dist, rewd = self.update_probe(step_idx=s, total_steps=total_steps)
            if s % 100 == 0:
                print(f"[{time.time()-t_start:6.2f}s] Step {s:4} | Dist: {dist:8.2f} | Reward: {rewd:10.2f} | Tick: {time.perf_counter()-t_step_start:.6f}s")
        
        print("\n>> DESCARGANDO MATRIZ DE SOLITONES (v13.0 - LOW ENERGY)...")
        df = pd.DataFrame(self.telemetry_buffer.cpu().numpy(), columns=['Px','Py','Pz','Vx','Vy','Vz','Tx','Ty','Tz'])
        df.to_csv('telemetry_soliton_agent0.csv', index=False)
        print(">> TELEMETRÍA DE LENTZ EXPORTADA.")

if __name__ == "__main__":
    forge = NGigaForgeBinary()
    forge.run_simulation(total_steps=2500)
