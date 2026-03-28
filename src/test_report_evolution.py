import os
import sys
import json
from unittest.mock import MagicMock, patch

# Añadir raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.swarm.report_manager import AutonomousReportManager

def test_genome_evolution_logic():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    manager = AutonomousReportManager(root_dir)
    
    # 1. Verificar carga de genoma inicial
    genome = manager._load_genome()
    print(f"[Test] Genoma inicial version: {genome.get('version')}")
    
    # 2. Simular evolución (Mutación manual para el test)
    mutated_genome = genome.copy()
    mutated_genome["version"] = "1.1.0-test"
    mutated_genome["layout"]["sections"] = ["rl_logic", "research_body"] # Cambiamos el orden
    
    with open(manager.genome_path, "w") as f:
        json.dump(mutated_genome, f, indent=4)
        
    print("[Test] 🧬 Mutación manual aplicada a v1.1.0-test.")
    
    # 3. Generar reporte con el nuevo ADN
    manager.mapper = MagicMock()
    manager.mapper.generate_thematic_map.return_value = "graph LR\nA-->B"
    manager.monitor = MagicMock()
    manager.monitor.get_system_health.return_value = ("OPTIMAL", {})
    
    print("[Test] Generando reporte evolutivo...")
    report_path = manager.build_premium_report("Test de evolución...", "Evolución")
    
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Verificar el orden cambiado: rl_logic antes que research_body
            if "System RL Logic" in content.split("---")[0] or "Gen 1.1.0-test" in content:
                print(f"[Test] ✅ Reporte refleja el ADN evolucionado (v1.1.0-test).")
            else:
                print(f"[Test] ❌ El reporte no refleja los cambios genéticos.")
        os.remove(report_path)
    
    # 4. Mockear evolve_genome real
    with patch.object(manager.mapper.kernel, "_call_groq", return_value='```json\n{"version": "2.0.0", "layout": {"sections": ["title"]}}\n```'):
        print("[Test] Probando evolve_genome() con Mock...")
        manager.drive = MagicMock() # Evitar subida real
        if manager.evolve_genome():
             print("[Test] ✅ evolve_genome() completó el ciclo con éxito.")
        else:
             print("[Test] ❌ evolve_genome() falló.")

    # Restaurar genoma original (opcional, pero buena práctica)
    with open(manager.genome_path, "w") as f:
        json.dump(genome, f, indent=4)

if __name__ == "__main__":
    test_genome_evolution_logic()
