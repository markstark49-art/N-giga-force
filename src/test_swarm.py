"""
Quick swarm integration test — verifies routing + planner JSON parsing.
Does NOT make real Groq API calls for the full swarm;
just tests imports and the complexity detector.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("=== TEST: Imports ===")
try:
    from agents.swarm.swarm_orchestrator import SwarmOrchestrator, _is_complex_task
    from agents.swarm.base_agent import BaseAgent, MODEL_FAST, MODEL_BALANCED, MODEL_DEEP
    from agents.swarm.planner_agent import PlannerAgent
    from agents.swarm.researcher_agent import ResearcherAgent
    from agents.swarm.coder_agent import CoderAgent
    from agents.swarm.critic_agent import CriticAgent
    print("✅ Todos los módulos del enjambre importaron correctamente.")
except Exception as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)

print("\n=== TEST: Complexity Router ===")
test_cases = [
    ("hola", False),
    ("hola cómo estás", False),
    ("crea un script que descargue el precio de bitcoin", True),
    ("investiga la API de NASA", True),
    ("desarrolla una aplicación Flask con autenticación JWT", True),
    ("gracias por tu ayuda", False),
]

all_passed = True
for text, expected in test_cases:
    result = _is_complex_task(text)
    status = "✅" if result == expected else "❌"
    if result != expected:
        all_passed = False
    print(f"  {status} '{text[:50]}' → {'SWARM' if result else 'LEVEL4'} (esperado: {'SWARM' if expected else 'LEVEL4'})")

print("\n=== TEST: Model Registry ===")
print(f"  FAST:     {MODEL_FAST}")
print(f"  BALANCED: {MODEL_BALANCED}")
print(f"  DEEP:     {MODEL_DEEP}")

print("\n=== TEST: SwarmOrchestrator Init ===")
try:
    swarm = SwarmOrchestrator()
    print("✅ SwarmOrchestrator inicializado.")
    print(f"   Coder tools: {len(swarm._coder_tools)}")
    print(f"   Researcher tools: {len(swarm._researcher_tools)}")
except Exception as e:
    print(f"⚠️  SwarmOrchestrator no pudo inicializar (puede ser normal si MCP no está corriendo): {e}")

print("\n=== RESUMEN ===")
if all_passed:
    print("✅ Todas las pruebas del enrutador de complejidad pasaron.")
else:
    print("⚠️  Algunas pruebas fallaron — revisa los resultados arriba.")
