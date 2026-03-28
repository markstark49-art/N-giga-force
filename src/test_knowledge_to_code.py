import os
import sys
import json
from unittest.mock import MagicMock

# Añadir raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.swarm.evolution_engine import EvolutionEngine
from agents.swarm.recursive_kernel_optimizer import RecursiveKernelOptimizer

def test_knowledge_injection_flow():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    evo = EvolutionEngine()
    rsi = RecursiveKernelOptimizer(root_dir)
    
    # 1. Simular descubrimiento
    insight = "OPTIMIZACIÓN DE ESTRUCTURA: Usar hashing para indexación rápida en 2 TB."
    print(f"[Test] Inyectando hallazgo: {insight[:30]}...")
    evo.inject_discovery_context(insight)
    
    # 2. Verificar persistencia de directiva
    directives_path = os.path.join(root_dir, "agents", "swarm", "evolutionary_directives.json")
    if os.path.exists(directives_path):
        with open(directives_path, "r", encoding="utf-8") as f:
            directives = json.load(f)
            if any(insight[:100] in d["key_insight"] for d in directives):
                print("[Test] ✅ Directiva guardada en JSON.")
            else:
                print("[Test] ❌ Directiva no encontrada en JSON.")
    else:
        print("[Test] ❌ No se creó evolutionary_directives.json.")

    # 3. Simular generación de variante con RSI
    dummy_file = os.path.join(root_dir, "agents", "swarm", "evolution_kernel.py")
    if not os.path.exists(dummy_file):
        # Crear dummy si no existe para el test
        with open(dummy_file, "w") as f: f.write("print('hello')")
        
    print("[Test] Generando variante RSI con conocimiento inyectado...")
    variant_path = rsi.generate_variant("agents/swarm/evolution_kernel.py")
    
    if os.path.exists(variant_path):
        with open(variant_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "[EVOLUTIONARY DIRECTIVES INJECTED]" in content and "Optimización" in content:
                print("[Test] ✅ Conocimiento inyectado exitosamente en el código de la variante.")
            else:
                print(f"[Test] ❌ El código de la variante no contiene las directivas. Cabecera: {content[:200]}")
        os.remove(variant_path)

if __name__ == "__main__":
    test_knowledge_injection_flow()
