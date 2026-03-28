"""
🧪 Test Percepción 360 — Validación del Bucle Sensorial
"""
import os
import sys
import json
from datetime import datetime

# Añadir raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.swarm.perceptor_visual import PerceptorVisual

def test_visual_perception():
    print("--- INICIANDO TEST PERCEPCIÓN 360 ---")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    perceptor = PerceptorVisual(root_dir)
    
    # 1. Simular un estado "Sano"
    print("\n[Escenario 1] Estado Óptimo")
    healthy_state = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "widgets": {"console_active": True, "infra_active": True},
        "recent_logs": "Bucle de autonomía funcionando. Todo OK.",
        "version": "v16.0.1"
    }
    state_path = os.path.join(root_dir, "agents", "swarm", "hud_state_capture.json")
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(healthy_state, f)
        
    health = perceptor.analyze_ui_health()
    print(f"Resultado: {health['status']} (Score: {health['score']})")
    
    # 2. Simular un estado "Crítico" (Errores en logs)
    print("\n[Escenario 2] Estado Crítico (Errores detectados)")
    broken_state = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "widgets": {"console_active": True},
        "recent_logs": "CRITICAL Error: Connection failed to satellite 8081. Exception: Timeout.",
        "version": "v16.0.1"
    }
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(broken_state, f)
        
    health = perceptor.analyze_ui_health()
    print(f"Resultado: {health['status']} (Score: {health['score']})")
    print(f"Issues: {health['issues']}")
    
    # 3. Simular un estado "Fallback" (Consola desaparecida)
    print("\n[Escenario 3] Estado de Precaución (Widgets desaparecidos)")
    ghost_state = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "widgets": {"console_active": False},
        "recent_logs": "",
        "version": "v16.0.1"
    }
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(ghost_state, f)
        
    health = perceptor.analyze_ui_health()
    print(f"Resultado: {health['status']} (Score: {health['score']})")
    
    print("\n--- TEST PERCEPCIÓN COMPLETADO ---")

if __name__ == "__main__":
    test_visual_perception()
