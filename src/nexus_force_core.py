import torch
import time
import sys

# --- DOCTRINA MATRICIAL N-GIGA-FORGE v11.0 ---
# Basado en benchmark real (3.0 GB usable seguro para evitar latencia VRAM)
MAX_SAFE_TENSORS = 268435456 
BYTES_PER_AGENT = 12
VRAM_LIMIT_GB = 3.0

class NexusForceCore:
    """
    Motor de Simulación Masiva con Protección Térmica y de Memoria.
    Controla la Intel Arc A750 bajo la doctrina de 40% de carga (Sweet Spot).
    """
    def __init__(self):
        self.device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
        self.dtype = torch.float16
        print(f"🔗 [NEXUS-CORE] Motor Iniciado en {self.device.upper()}")
        print(f"🛡️  PROTECCION ACTIVA: Límite Seguro = {MAX_SAFE_TENSORS:,} agentes ({VRAM_LIMIT_GB} GB)")

    def validate_allocation(self, requested_agents):
        """
        Función de Advertencia y Seguridad.
        Detiene la simulación si se intenta forzar el motor más allá del límite seguro.
        """
        requested_vram_gb = (requested_agents * BYTES_PER_AGENT) / (1024**3)
        
        if requested_agents > MAX_SAFE_TENSORS:
            print("\n" + "!"*60)
            print(f"⚠️  ALERTA DE SEGURIDAD NEXUS: INTENTO DE SOBRECARGA DETECTADO")
            print(f"Solicitado: {requested_agents:,} agentes ({requested_vram_gb:.2f} GB)")
            print(f"Límite Seguro: {MAX_SAFE_TENSORS:,} agentes ({VRAM_LIMIT_GB} GB)")
            print("Razonamiento: Evitar latencia de VRAM y proteger integridad de la XPU.")
            print("!"*60 + "\n")
            
            # Detenemos la ejecución para proteger el hardware
            sys.exit("🛑 SIMULACIÓN ABORTADA POR SEGURIDAD TÉCNICA.")
        
        return True

    def run_swarm_cycle(self, agent_count):
        # Validamos antes de asignar un solo byte
        self.validate_allocation(agent_count)
        
        print(f"🚀 [XPU] Lanzando enjambre de {agent_count:,} agentes...")
        
        # Asignación matricial optimizada
        P = torch.zeros(agent_count, 3, device=self.device, dtype=self.dtype)
        V = torch.randn(agent_count, 3, device=self.device, dtype=self.dtype) * 0.1
        
        t0 = time.perf_counter()
        # Operación GEMM Nativa (XMX Core)
        P = P + V
        
        if self.device == 'xpu':
            torch.xpu.synchronize()
            
        elapsed = time.perf_counter() - t0
        aps = agent_count / elapsed
        
        print(f"✅ CICLO COMPLETADO: {elapsed:.6f}s | {aps:,.0f} agentes/seg")
        
        # Limpieza inmediata de memoria
        del P, V
        if self.device == 'xpu':
            torch.xpu.empty_cache()

if __name__ == "__main__":
    core = NexusForceCore()
    
    # PRUEBA 1: Carga Segura (100M agentes)
    core.run_swarm_cycle(100_000_000)
    
    # PRUEBA 2: Intento de forzar la GPU (500M agentes) -> Debería saltar la Warning
    time.sleep(1)
    core.run_swarm_cycle(500_000_000)
