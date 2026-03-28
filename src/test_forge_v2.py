import time
import ast
import random

def legacy_text_mutation(file_content, comment):
    """Simulaci?n de edici?n de texto legacy (search & replace)."""
    return f'"{comment}"\n' + file_content

def forge_ast_mutation(file_content, comment):
    """Mutaci?n at?mica real usando el motor AST."""
    tree = ast.parse(file_content)
    comment_node = ast.Expr(value=ast.Constant(value=f"AUDIT_FORGE: {comment}"))
    tree.body.insert(0, comment_node)
    return ast.unparse(tree)

def run_benchmark():
    print("🧬 [NEXUS FORGE] INICIANDO BENCHMARK DE SINGULARIDAD...")
    
    with open("agents/swarm/neural_hud.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Pruebas de velocidad
    start = time.time()
    for _ in range(100):
        _ = legacy_text_mutation(content, "Test")
    legacy_time = (time.time() - start) / 100
    
    start = time.time()
    for _ in range(100):
        _ = forge_ast_mutation(content, "Test")
    forge_time = (time.time() - start) / 100

    print(f"\n⚡ RESULTADOS DE VELOCIDAD (Promedio 100 ciclos):")
    print(f"   Legacy Text: {legacy_time:.6f}s")
    print(f"   Nexus Forge (AST): {forge_time:.6f}s")

    # VALIDACION DE SEGURIDAD (Prueba de Fuego)
    print("\n🔥 [PRUEBA DE FUEGO] INYECTANDO NOTA DE AUDITORIA REAL...")
    try:
        # Aquí crearíamos una instancia temporal de NexusForge para la prueba
        from agents.swarm.neural_hud import NexusForge, QualityJudge
        import tkinter as tk
        
        dummy_canvas = tk.Canvas() # Solo para el test
        qj = QualityJudge(dummy_canvas, 0, 0)
        nf = NexusForge(dummy_canvas, 1300, 100)
        nf.set_judge(qj)
        
        success = nf.forge_atomic_comment("agents/swarm/neural_hud.py", f"Benchmark Pass {datetime.now()}")
        if success:
            print("✅ MUTACION EXITOSA: Nota inyectada en el AST de neural_hud.py")
        else:
            print("❌ MUTACION VETADA por el Quality Judge (Seguridad activa)")
            
    except Exception as e:
        print(f"⚠️ ERROR DURANTE LA PRUEBA: {str(e)}")

if __name__ == "__main__":
    from datetime import datetime
    run_benchmark()
