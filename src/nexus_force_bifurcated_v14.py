import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import time
import sys

# === HEMISFERIO DERECHO: NTM CORE (RECONSTRUCCIÓN V14) ===

class NTMMemoryBank(nn.Module):
    def __init__(self, mem_size, mem_dim, dtype, device):
        super(NTMMemoryBank, self).__init__()
        self.mem_size = mem_size
        self.mem_dim = mem_dim
        self.device = device
        self.dtype = dtype
        
        # Buffer de memoria M [N_size x M_dim]
        self.register_buffer('M', torch.full((mem_size, mem_dim), 1e-6, dtype=dtype, device=device))
        
        # Pesos de direccionamiento previos (Inicialización uniforme)
        self.register_buffer('prev_w_read', torch.full((1, mem_size), 1.0 / mem_size, dtype=dtype, device=device))
        self.register_buffer('prev_w_write', torch.full((1, mem_size), 1.0 / mem_size, dtype=dtype, device=device))

    def read(self, w):
        """Lectura: r = sum(w_i * M_i)"""
        return torch.matmul(w, self.M)

    def write(self, w, erase, add):
        """Escritura: M = M_old * (1 - w * erase) + w * add"""
        # Erase: w y erase son [1 x N] y [1 x M] -> Outer product [N x M]
        erase_matrix = torch.matmul(w.transpose(0, 1), erase)
        self.M.mul_(1 - erase_matrix)
        
        # Add: Outer product [N x M]
        add_matrix = torch.matmul(w.transpose(0, 1), add)
        self.M.add_(add_matrix)

class NTMHeadV14(nn.Module):
    def __init__(self, controller_dim, mem_dim, mem_size, dtype, device):
        super(NTMHeadV14, self).__init__()
        self.mem_size = mem_size
        self.mem_dim = mem_dim
        
        # Proyección del controlador a parámetros NTM
        # k (dim), beta (1), g (1), s (3), gamma (1) + Erase (dim) + Add (dim)
        self.total_params = mem_dim + 1 + 1 + 3 + 1 + mem_dim * 2
        self.project = nn.Linear(controller_dim, self.total_params).to(dtype).to(device)

    def def_addressing(self, h, prev_w, M):
        """Direccionamiento de Graves (Content + Location)"""
        params = self.project(h)
        
        # 1. Separación de parámetros
        k = torch.tanh(params[:, :self.mem_dim])
        beta = F.softplus(params[:, self.mem_dim : self.mem_dim+1])
        g = torch.sigmoid(params[:, self.mem_dim+1 : self.mem_dim+2])
        s = F.softmax(params[:, self.mem_dim+2 : self.mem_dim+5], dim=-1) # Shift circular (-1, 0, 1)
        gamma = 1.0 + F.softplus(params[:, self.mem_dim+5 : self.mem_dim+6])
        
        # 2. Content Addressing (Similitud del Coseno)
        cosine_sim = F.cosine_similarity(k.unsqueeze(1), M, dim=-1)
        w_c = F.softmax(beta * cosine_sim, dim=-1)
        
        # 3. Interpolación (Gating)
        w_g = g * w_c + (1 - g) * prev_w
        
        # 4. Convolutional Shift (Shift Circular)
        w_s = self._circular_convolution(w_g, s)
        
        # 5. Sharpening
        w_p = w_s ** gamma
        w = w_p / (torch.sum(w_p, dim=-1, keepdim=True) + 1e-12)
        
        return w, params

    def _circular_convolution(self, w, s):
        """Implementación de shift circular para direccionamiento relativo"""
        size = self.mem_size
        temp = torch.cat([w[:, -1:], w, w[:, :1]], dim=-1) # Padding circular para kernel 3
        # Convolución 1D manual para 3 pesos de s (shift -1, 0, 1)
        res = (s[:, 0:1] * temp[:, 0:size] + 
               s[:, 1:2] * temp[:, 1:size+1] + 
               s[:, 2:3] * temp[:, 2:size+2])
        return res

# === CEREBRO BIFURCADO MASTER CORE: SINGULARIDAD DE PLANCK ===

class BifurcatedBrainPlanck:
    def __init__(self, device="xpu"):
        self.device = device
        self.dtype_physics = torch.float16
        self.dtype_logic = torch.float32 
        
        # --- HEMISFERIO IZQUIERDO: ESCALA FERMI (100% Inercial) ---
        self.num_agents = 268435456  # 2^28 Agentes Exactos
        print(f"🌌 Inicializando Singularidad de Planck: {self.num_agents:,} Agentes (FP16)...")
        
        try:
            self.P_enjambre = torch.zeros((self.num_agents, 3), dtype=self.dtype_physics, device=device)
            self.V_enjambre = torch.zeros((self.num_agents, 3), dtype=self.dtype_physics, device=device)
            print(f"✅ VRAM RESERVADA: 3.21 GB (Cero Fricción)")
        except RuntimeError:
            print("❌ VRAM Insuficiente.")
            sys.exit(1)
        
        self.R_burbuja = torch.tensor(50.0, dtype=self.dtype_physics, device=device)
        self.sigma = torch.tensor(8.0, dtype=self.dtype_physics, device=device)
        
        # Stream Asíncrono
        if device == "xpu":
            self.physics_stream = torch.xpu.Stream()
        elif device == "cuda":
            self.physics_stream = torch.cuda.Stream()
        else:
            self.physics_stream = None

        # --- HEMISFERIO DERECHO: RAZONAMIENTO LÓGICO ---
        print("🧠 Inicializando NTM Logic Core (FP32)...")
        self.mem_size = 128
        self.mem_dim = 64
        self.controller_dim = 128
        
        # LSTM Controller + Razonamiento NTM
        self.controller = nn.LSTMCell(self.mem_dim * 2, self.controller_dim).to(self.dtype_logic).to(device)
        self.memory = NTMMemoryBank(self.mem_size, self.mem_dim, self.dtype_logic, device)
        self.heads = NTMHeadV14(self.controller_dim, self.mem_dim, self.mem_size, self.dtype_logic, device)
        
        self.h_state = torch.zeros((1, self.controller_dim), dtype=self.dtype_logic, device=device)
        self.c_state = torch.zeros((1, self.controller_dim), dtype=self.dtype_logic, device=device)
        self.prev_read_vec = torch.zeros((1, self.mem_dim), dtype=self.dtype_logic, device=device)

    @torch.no_grad()
    def step_instinct_físico_planck(self, v_warp_vec):
        v_warp = v_warp_vec.to(self.dtype_physics)
        pos_nave = self.P_enjambre[0].clone()
        chunk_size = 16777216
        
        # Dispatch Asíncrono
        context = torch.xpu.stream(self.physics_stream) if self.device == "xpu" else torch.cuda.stream(self.physics_stream) if hasattr(torch, 'cuda') and self.device == 'cuda' else torch.no_grad()
        
        with context:
            for i in range(1, self.num_agents, chunk_size):
                end = min(i + chunk_size, self.num_agents)
                r_mag = self.P_enjambre[i:end].sub(pos_nave).pow_(2).sum(dim=1, keepdim=True).add_(1e-6).sqrt_()
                f_r = torch.tanh(self.sigma * (r_mag + self.R_burbuja)).sub_(torch.tanh(self.sigma * (r_mag - self.R_burbuja))).div_(2.0)
                
                # FASE 3: Desplazamiento (Corregido para Broadcasting [Chunk, 3])
                desplazamiento = f_r * v_warp
                
                self.P_enjambre[i:end].add_(desplazamiento)
                self.V_enjambre[i:end].add_(desplazamiento, alpha=0.005)
                del r_mag, f_r, desplazamiento

    def step_razonamiento_lógico(self, input_token):
        x = torch.cat([input_token.to(self.dtype_logic), self.prev_read_vec], dim=-1)
        self.h_state, self.c_state = self.controller(x, (self.h_state, self.c_state))
        
        w_read, _ = self.heads.def_addressing(self.h_state, self.memory.prev_w_read, self.memory.M)
        w_write, write_params = self.heads.def_addressing(self.h_state, self.memory.prev_w_write, self.memory.M)
        
        # Erase: sigmoid, Add: tanh (Final de write_params)
        erase_vec = torch.sigmoid(write_params[:, -self.mem_dim*2 : -self.mem_dim])
        add_vec = torch.tanh(write_params[:, -self.mem_dim:])
        
        self.prev_read_vec = self.memory.read(w_read)
        self.memory.write(w_write, erase_vec, add_vec)
        
        self.memory.prev_w_read = w_read
        self.memory.prev_w_write = w_write
        
        return self.h_state

if __name__ == "__main__":
    device = "xpu" if hasattr(torch, "xpu") and torch.xpu.is_available() else "cpu"
    brain = BifurcatedBrainPlanck(device=device)
    
    t_frame = time.perf_counter()
    v_warp = torch.tensor([0.001, 0.0, 0.0], dtype=torch.float16, device=device)
    brain.step_instinct_físico_planck(v_warp)
    
    input_token = torch.randn((1, brain.mem_dim), device=device)
    logic_output = brain.step_razonamiento_lógico(input_token)
    
    if device == "xpu": torch.xpu.synchronize()
    
    print(f"✅ Frame Asíncrono Completado: {time.perf_counter()-t_frame:.4f}s.")
    print(f"🧠 Salida NTM (Lógica): {logic_output[0, :5].cpu().detach().numpy()}...")
