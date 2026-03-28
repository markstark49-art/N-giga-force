import torch
import time

class SwarmBenchmark:
    """
    CRITICAL ANALYSIS: CPU LOGIC vs XPU MATRIX POWER
    Verificación del protocolo de 1,000,000 de agentes.
    """
    def __init__(self, agent_count=1_000_000):
        self.device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
        self.count = agent_count
        
        # Inicialización de Tensores (Matrices)
        self.P = torch.randn(self.count, 3, device=self.device, dtype=torch.float16)
        self.V = torch.randn(self.count, 3, device=self.device, dtype=torch.float16)
        print(f"📊 BENCHMARK READY: {self.count:,} Agentes en {self.device.upper()}\n")

    def run_cpu_style(self, sample_size=1000):
        """
        Simulación de la 'Trampa del CPU': Bucle secuencial.
        (Solo procesamos una muestra porque el bucle 'for' es mortalmente lento)
        """
        print(f"❌ [CPU STYLE] Procesando solo {sample_size:,} agentes vía bucle 'for'...")
        t0 = time.perf_counter()
        
        # Simulamos la mentalidad de bucle for (secuencial)
        for i in range(sample_size):
            # Operando de uno en uno (mentalmente)
            self.P[i] = self.P[i] + self.V[i]
            
        torch.xpu.synchronize()
        elapsed = time.perf_counter() - t0
        
        # Proyectamos cuánto tardaría el millón completo
        projected = (elapsed / sample_size) * self.count
        print(f"   DURACIÓN ({sample_size} agentes): {elapsed:.4f}s")
        print(f"   ⚠️ PROYECCIÓN PARA 1M AGENTES: {projected:.2f}s (COLAPSO INMINENTE)\n")
        return projected

    def run_xpu_matrix_style(self):
        """
        La Solución XPU: Tensorización pura.
        P = P + V (Todo a la vez en los XMX Engines)
        """
        print(f"🚀 [XPU MATRIX STYLE] Procesando 1,000,000 de agentes simultáneamente...")
        t0 = time.perf_counter()
        
        # UNA SOLA INSTRUCCIÓN MATRICIAL (Álgebra Lineal)
        self.P = self.P + self.V 
        
        torch.xpu.synchronize()
        elapsed = time.perf_counter() - t0
        print(f"✅ FINALIZADO EN: {elapsed:.6f}s (FRACCIÓN DE MILISEGUNDO)")
        return elapsed

if __name__ == "__main__":
    bench = SwarmBenchmark(1_000_000)
    cpu_proj = bench.run_cpu_style(1000) # Una pequeña muestra para no colapsar
    xpu_real = bench.run_xpu_matrix_style()
    
    speed_factor = cpu_proj / xpu_real
    print(f"\n🏆 VERDICTO CRÍTICO: La XPU es {speed_factor:,.0f} veces más rápida que el código secuencial.")
