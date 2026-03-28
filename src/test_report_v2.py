import os
import sys
from unittest.mock import MagicMock, patch

# Añadir raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.swarm.report_manager import AutonomousReportManager

def test_premium_report_logic():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = AutonomousReportManager(root_dir)
    
    # Mocking external components
    manager.drive = MagicMock()
    manager.drive.find_folder.return_value = "folder_id"
    manager.drive.upload_file.return_value = "file_id"
    
    manager.mapper = MagicMock()
    manager.mapper.generate_thematic_map.return_value = "graph LR\nA-->B"
    
    manager.monitor = MagicMock()
    manager.monitor.get_system_health.return_value = ("OPTIMAL", {"cpu": 10, "ram": 20, "vram_percent": 30})
    
    # Test data
    sample_text = "El multiverso es una teoría fascinante sobre la existencia de múltiples universos paralelos."
    
    print("[Test] Generando reporte premium...")
    report_path = manager.build_premium_report(sample_text, "Multiverso")
    
    if os.path.exists(report_path):
        print(f"[Test] ✅ Reporte generado en: {report_path}")
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "```mermaid" in content and "Telemetría" in content:
                print("[Test] ✅ Contenido verificado: Mermaid y Telemetría presentes.")
            else:
                print("[Test] ❌ Contenido incompleto.")
        
        # Sincronización simulada
        success = manager.sync_to_cloud(report_path)
        if success:
            print("[Test] ✅ Sincronización simulada exitosa.")
            
        # Cleanup
        os.remove(report_path)
    else:
        print("[Test] ❌ No se generó el archivo.")

if __name__ == "__main__":
    test_premium_report_logic()
