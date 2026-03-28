import torch
import time
import sys

# --- NEXUS-FORGE: XMX EXTREME STRESS KERNEL v11.2 ---
# Objetivo: Medir el throughput máximo y la estabilidad térmica de la Arc A750.
# NO USAR EN SISTEMAS CON REFRIGERACIÓN DEFECTUOSA.

class XMXExtremeStress:
    def __init__(self, matrix_size=8192):
        self.device = 'xpu' if hasattr(torch, 'xpu') and torch.xpu.is_available() else 'cpu'
        self.size = matrix_size
        
        print("\n" + "="*60)
        print("🔥 [XMX-STRESS-CORE] INICIANDO PRUEBA DE FUEGO")
        print(f"HW: Intel Arc A750 (XPU) | Matriz: {matrix_size}x{matrix_size}")
        print(f"Modo: FP32 (Carga Máxima de Silicio)")
        print("="*60 + "\n")

    def run_stress_test(self, iterations=50):
        # Asignación de matrices densas (8192x8192 ocupa ~256MB cada una en FP32)
        # Necesitaremos 3 matrices: (~768MB de VRAM pura de impacto)
        A = torch.randn(self.size, self.size, device=self.device, dtype=torch.float)
        B = torch.randn(self.size, self.size, device=self.device, dtype=torch.float)
        
        print(f"⚙️  [STEP 1] Matrices A y B generadas. Iniciando {iterations} multiplicaciones masivas...")
        
        t_start = time.perf_counter()
        
        try:
            for i in range(1, iterations + 1):
                t0 = time.perf_counter()
                
                # LA OPERACIÓN MAESTRA: Multiplicación de Matrices (Dense GEMM)
                # Esto activa el 100% de los motores XMX
                C = torch.matmul(A, B)
                
                if self.device == 'xpu':
                    torch.xpu.synchronize()
                
                t1 = time.perf_counter()
                elapsed = t1 - t0
                
                # Calcular TFLOPS (TeraFLOPS)
                # Formula: (2 * N^3) / tiempo
                tflops = (2.0 * (self.size**3)) / (elapsed * 1e12)
                
                if i % 5 == 0 or i == 1:
                    print(f"🔄 Iteración {i:2d}/{iterations} | Latencia: {elapsed:.4f}s | Potencia: {tflops:.2f} TFLOPS")
            
            t_total = time.perf_counter() - t_start
            print(f"\n✅ [STATS] Stress completo en {t_total:.2f}s")
            print(f"🏆 RENDIMIENTO SOSTENIDO: { ( (2.0 * iterations * (self.size**3)) / (t_total * 1e12) ):.2f} TFLOPS")
            
        except Exception as e:
            print(f"\n❌ FALLO TÉCNICO DURANTE EL STRESS: {e}")
        
        finally:
            del A, B, C
            if self.device == 'xpu':
                torch.xpu.empty_cache()

if __name__ == "__main__":
    # Ajustamos el tamaño a 8192 para una carga óptima en la Arc A750
    tester = XMXExtremeStress(matrix_size=8192)
    tester.run_stress_test(iterations=50)
