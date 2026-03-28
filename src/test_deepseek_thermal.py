import os
import sys
import time
import random

def run_deepseek_thermal_benchmark():
    print("🛡️ [BENCHMARK] ESCUDO T?RMICO: DEEPSEEK CODER + INTEL ARC A750")
    print("🔥 OBJETIVO: Estresar la VRAM y validar el Safety Lock.")
    
    # Importar componentes de Cogni Swarm
    from agents.swarm.neural_hud import NexusForge, IntelXPUBridge, QualityJudge
    import tkinter as tk
    import types
    
    root = tk.Tk()
    root.withdraw()
    canvas = tk.Canvas(root)
    
    nf = NexusForge(canvas, 0, 0)
    xpu = IntelXPUBridge(canvas, 0, 0)
    qj = QualityJudge(canvas, 0, 0)
    nf.set_judge(qj)
    
    # Inyecci?n Din?mica (Sincronizaci?n manual para el test)
    def forge_triton_kernel_injected(self, xpu_bridge, kernel_name, op_matrix):
        return xpu_bridge.generate_triton_jit_template(kernel_name, op_matrix)
    
    nf.forge_triton_kernel = types.MethodType(forge_triton_kernel_injected, nf)

    # SIMULACI?N DE R?FAGA DE DEEPSEEK CODER
    for i in range(1, 10):
        print(f"\n🛰️ [DEEPSEEK] Enviando r?faga l?gica #{i}...")
        
        kernel_name = f"deepseek_optimization_{i}"
        jit_code = nf.forge_triton_kernel(xpu, kernel_name, "matmul")
        
        if "[ERROR]" in jit_code or "[SAFETY]" in jit_code:
            print(f"🛑 [SAFETY] BLOQUEO ACTIVADO EN R?FAGA #{i}")
            print(f"📊 Estado Final - VRAM: {xpu.vram_used} | TEMP: {int(xpu.temp_logic)}?C")
            print("✅ ?XITO: La GPU ha sido salvada del sobrecalentamiento.")
            break
        else:
            print(f"✅ Kernel #{i} Forjado. VRAM actual: {xpu.vram_used} | TEMP: {int(xpu.temp_logic)}?C")
        
        time.sleep(0.2) # R?faga r?pida

    root.destroy()

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    run_deepseek_thermal_benchmark()
