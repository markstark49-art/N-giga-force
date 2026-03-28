import os
import sys

# Añadir la carpeta raíz al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from agents.swarm.evolution_kernel import EvolutionaryKernel

def run_gpu_test():
    print("🚀 Iniciando prueba de aceleración GPU...")
    kernel = EvolutionaryKernel()
    
    # Archivo de prueba
    test_file = "agents/reasoning/model_router.py"
    
    print(f"🤖 Solicitando optimización para {test_file} usando perfil GPU...")
    
    # Le pedimos solo una pequeña función para que sea rápido
    optimized_code, chunk_info = kernel.ask_for_optimization(test_file, chunk_name="select_model")
    
    if optimized_code:
        print("✅ ¡ÉXITO! El modelo respondió.")
        print("-" * 30)
        print(optimized_code[:200] + "...")
        print("-" * 30)
        print("💡 Verifica tu Administrador de Tareas: La VRAM debería haber subido y la RAM bajado.")
    else:
        print("❌ El modelo no respondió.")

if __name__ == "__main__":
    run_gpu_test()
