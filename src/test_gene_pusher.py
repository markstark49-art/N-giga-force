import os
import sys
import json
from unittest.mock import MagicMock, patch

# Añadir raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.swarm.gene_pusher import GenePusher

def test_gene_pusher_logic():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pusher = GenePusher(root_dir)
    
    # Mocking components to avoid real Google Drive API calls
    pusher.drive = MagicMock()
    pusher.drive.find_folder.return_value = "folder_id_123"
    pusher.drive.create_folder.return_value = "folder_id_456"
    pusher.drive.upload_file.return_value = "file_id_789"
    
    # Mocking version manager
    pusher.version_mgr = MagicMock()
    pusher.version_mgr.get_current_version_str.return_value = "v1.90.0"
    
    # Mocking evolution log content
    test_log = os.path.join(root_dir, "test_evolution_history.md")
    with open(test_log, "w", encoding="utf-8") as f:
        f.write("## [2026-03-20 18:00:00] SNAPSHOT\n")
        f.write("Snapshot Somático creado: `mutant-test`\n")
        f.write("## [2026-03-20 18:05:00] MUTATION\n")
        f.write("Archivo mutado: `agents/swarm/gene_pusher.py`\n")
        f.write("## [2026-03-20 18:05:01] AUTO-EVOLVE\n")

    pusher.evolution_log = test_log
    
    # Run Push
    print("[Test] Corriendo run_push()...")
    with patch("os.path.exists", return_value=True):
        success = pusher.run_push()
        
    if success:
        print("[Test] ✅ GenePusher identificó la mutación y simuló la carga correctamente.")
    else:
        print("[Test] ❌ GenePusher falló en la lógica de detección o carga.")
    
    # Cleanup
    if os.path.exists(test_log):
        os.remove(test_log)

if __name__ == "__main__":
    test_gene_pusher_logic()
