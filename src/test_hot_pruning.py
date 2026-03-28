import os
import sys
import time
import ast
import random

# Definimos una clase "Obesa" para la prueba
OBESITY_FILE = "tmp_obese_component.py"
with open(OBESITY_FILE, "w") as f:
    f.write('''
class HeavyDataNode:
    def collect_all_metrics(self):
        # Esta es la ineficiencia: crea una lista masiva en RAM
        data = []
        for i in range(1000000):
            data.append(i * 1.5)
        return data
''')

def run_pruning_benchmark():
    print("🧠 [BENCHMARK] INICIANDO PODA DE MEMORIA EN CALIENTE...")
    
    # Importamos los componentes del HUD
    from agents.swarm.neural_hud import NexusForge, PruningAnalyzer, QualityJudge
    import tkinter as tk
    
    dummy_canvas = tk.Canvas()
    nf = NexusForge(dummy_canvas, 0, 0)
    qj = QualityJudge(dummy_canvas, 0, 0)
    pa = PruningAnalyzer(dummy_canvas, nf, 0, 0)
    nf.set_judge(qj)

    print(f"📊 Estado Inicial: {OBESITY_FILE} tiene un m?todo 'Return List' pesado.")
    
    # Ejecutamos la Poda
    start_time = time.perf_counter()
    success = pa.analyze_and_prune(OBESITY_FILE, "HeavyDataNode", "collect_all_metrics")
    end_time = time.perf_counter()
    
    if success:
        print(f"\n✅ PODA COMPLETADA en {end_time - start_time:.6f} segundos.")
        print(f"   Ahorro estimado: {pa.memory_saved} MB")
        
        # Verificamos la transformaci?n estructural
        with open(OBESITY_FILE, "r") as f:
            new_content = f.read()
            if "MEMORY OPTIMIZED" in new_content:
                print("✨ VERIFICACI?N: El ADN del componente ha sido aligerado con ?xito.")
                print("\n--- NUEVO ADN (Fragmento) ---")
                print(new_content)
    else:
        print("\n❌ FALLO EN LA PODA.")

if __name__ == "__main__":
    run_pruning_benchmark()
    # Limpieza
    if os.path.exists(OBESITY_FILE):
        os.remove(OBESITY_FILE)
