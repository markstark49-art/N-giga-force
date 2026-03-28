import time
import ast
import random
import os
import tkinter as tk

def run_benchmark_v2():
    print("🧬 [NEXUS FORGE v2] INICIANDO BENCHMARK DE ALTO RENDIMIENTO (BUFFER)...")
    
    file_path = "agents/swarm/neural_hud.py"
    with open(file_path, "r", encoding="utf-8") as f:
        source_content = f.read()

    # Importar clase real para el test
    from agents.swarm.neural_hud import NexusForge, QualityJudge
    
    dummy_canvas = tk.Canvas()
    nf = NexusForge(dummy_canvas, 1300, 100)
    qj = QualityJudge(dummy_canvas, 0, 0)
    nf.set_judge(qj)

    # 1. TEST DE CALENTAMIENTO (Primer Parseo)
    start = time.time()
    _ = nf.get_shadow_ast(file_path)
    cold_start_time = time.time() - start
    print(f"❄️ Cold Start (Primer Parseo): {cold_start_time:.6f}s")

    # 2. TEST DE BUFFER (Shadow Cache)
    start = time.time()
    for _ in range(1000): # 1000 repeticiones para ver la diferencia real
        _ = nf.get_shadow_ast(file_path)
    buffer_time = (time.time() - start) / 1000
    print(f"⚡ Buffer Access (Shadow Cache): {buffer_time:.8f}s")

    # 3. COMPARATIVA FINAL
    print(f"\n📈 ANALISIS DE EFICIENCIA:")
    gain = (cold_start_time / buffer_time) if buffer_time > 0 else 0
    print(f"   El Nexus Buffer es {gain:.1f} veces m?s r?pido que el parseo tradicional.")

    # 🔥 PRUEBA DE FUEGO (Mutaci?n de Alta Velocidad)
    print("\n🔥 [PRUEBA DE FUEGO] EJECUTANDO MUTACION ASINCRONA...")
    
    success = nf.forge_atomic_comment(file_path, f"High-Speed V2 Verified {datetime.now()}")
    
    if success:
        print("✅ EXITOSA: La mutaci?n fue forjada y aprobada instant?neamente.")
    else:
        print("🛡️ VETADA: Operaci?n segura, el Juez detuvo la mutaci?n (Comportamiento esperado).")

if __name__ == "__main__":
    from datetime import datetime
    run_benchmark_v2()
