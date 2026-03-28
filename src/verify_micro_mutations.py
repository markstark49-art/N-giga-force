import os
import sys
import random

# Root path
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)

from agents.swarm.evolution_kernel import EvolutionaryKernel

def test_ast_surgery():
    kernel = EvolutionaryKernel(root)
    test_file = "agents/reasoning/model_router.py"
    
    # 1. Test Chunk extraction
    with open(os.path.join(root, test_file), "r", encoding="utf-8") as f:
        content = f.read()
    
    chunks = kernel._get_code_chunks(content)
    print(f"--- 🧪 PRUEBA DE CIRUGÍA AST ---")
    print(f"Fragmentos detectados en {test_file}: {len(chunks)}")
    for c in chunks:
        print(f" - [{c['type']}] {c['name']} (Líneas {c['start_line']+1}-{c['end_line']})")
    
    if not chunks:
        print("❌ ERROR: No se detectaron fragmentos.")
        return

    # 2. Test Optimization of a single chunk
    target = chunks[0]
    print(f"\n🚀 Intentando optimizar micro-fragmento: {target['name']}...")
    new_chunk, info = kernel.ask_for_optimization(test_file, chunk_name=target['name'])
    
    if new_chunk:
        print(f"✅ Optimización recibida ({len(new_chunk)} chars)")
        # 3. Test Reinsertion
        new_content = kernel._replace_chunk_in_content(content, info, new_chunk)
        if target['name'] in new_content and len(new_content) > 100:
            print(f"✅ Cirugía exitosa. Tamaño final: {len(new_content)} chars.")
            
            # Verificación visual (primeras 5 líneas del nuevo chunk)
            print("\nPreview del código mutado:")
            print("\n".join(new_content.splitlines()[info['start_line'] : info['start_line']+5]))
        else:
            print("❌ ERROR: La cirugía falló.")
    else:
        print("❌ FALLO: El modelo no devolvió código.")

if __name__ == "__main__":
    test_ast_surgery()
