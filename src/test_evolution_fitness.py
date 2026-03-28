import sys
import os
import time

# Root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.swarm.evolution_kernel import EvolutionaryKernel

def run_fitness_test():
    kernel = EvolutionaryKernel()
    rel_path = "script_a_optimizar.py"
    
    print("--- 🧬 TEST DE SELECCIÓN NATURAL (FITNESS) ---")
    
    # 1. Snapshot original
    sid = kernel.create_evolution_snapshot()
    
    # 2. Mutación: Versión optimizada (iterativa)
    optimized_code = """import time
def calcular_fibonacci(n):
    # Versión OPTIMIZADA (iterativa)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == "__main__":
    result = calcular_fibonacci(30)
    print(result)
"""
    
    print("\n[Aptitud] Aplicando mutación optimizada...")
    kernel.safe_mutate(rel_path, optimized_code)
    
    # 3. Evaluar Aptitud contra el original (que está en el snapshot)
    # Para comparar, el kernel necesita ejecutar el script mutado y el original.
    # El método evaluate_evolution asume que el mutado está en disco.
    
    score = kernel.evaluate_evolution(rel_path, rel_path)
    
    if score > 100: # Base score para AST ok + Correctness
        print(f"\n✅ ÉXITO: La mutación es superior (Score: {score:.2f}). Evolution permanente.")
    else:
        print(f"\n❌ FRACASO: La mutación no superó al original. Realizando ROLLBACK.")
        kernel.rollback_to_snapshot(sid)

if __name__ == "__main__":
    run_fitness_test()
