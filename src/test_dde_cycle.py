import os
import sys
from unittest.mock import MagicMock, patch

# Añadir raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.swarm.report_manager import AutonomousReportManager

def test_dde_functionality():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = AutonomousReportManager(root_dir)
    
    # Mocking external components
    manager.drive = MagicMock()
    manager.drive.find_folder.return_value = "fake_folder_id"
    manager.drive.create_folder.return_value = "fake_folder_id"
    manager.drive.upload_file.return_value = "fake_file_id"
    manager.mapper = MagicMock()
    manager.mapper.generate_thematic_map.return_value = "graph LR\nA-->B"
    manager.monitor = MagicMock()
    manager.monitor.get_system_health.return_value = ("OPTIMAL", {})
    
    topic = "Fisica Cuantica"
    
    # 1. Probar creación de bóveda
    vault_id = manager.create_discovery_vault(topic)
    print(f"[Test] ID de Bóveda creado: {vault_id}")
    
    # 2. Probar reporte secuencial (Paso 1)
    print("[Test] Generando reporte Paso 1...")
    report_path = manager.build_premium_report("Datos iniciales sobre el entrelazamiento.", topic, step_number=1)
    
    if os.path.exists(report_path):
        filename = os.path.basename(report_path)
        print(f"[Test] Archivo generado: {filename}")
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "Paso 1/4" in content and filename.startswith("step1_"):
                 print("[Test] ✅ Reporte Paso 1 verificado correctamente.")
            else:
                 print(f"[Test] ❌ Error en el formato del reporte Paso 1. Contenido inicial: {content[:100]}")
        os.remove(report_path)
        
    # 3. Probar sincronización dirigida
    success = manager.sync_to_cloud("fake_path_exists_in_mock", discovery_folder_id=vault_id)
    with patch("os.path.exists", return_value=True):
        if manager.sync_to_cloud("dummy.md", discovery_folder_id=vault_id):
            print("[Test] ✅ Sincronización a Bóveda verificada.")

if __name__ == "__main__":
    test_dde_functionality()
