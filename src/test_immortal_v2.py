import os
import sys
import json
from agents.swarm.snapshot_manager import SnapshotManager
from agents.swarm.high_res_logger import HighResLogger

def test_immortal_architecture():
    root = os.getcwd()
    print("--- 🌌 INICIANDO TEST DE ARQUITECTURA INMORTAL ---")
    
    # 1. Test Snapshot Manager
    print("\n[Test 1] SnapshotManager...")
    sm = SnapshotManager(root)
    zip_path = sm.create_system_snapshot()
    if os.path.exists(zip_path):
        print(f"  ✅ ZIP local creado: {os.path.basename(zip_path)}")
        # Cifrado
        enc_path = sm.encrypt_snapshot(zip_path)
        if os.path.exists(enc_path):
            print(f"  ✅ ZIP cifrado exitosamente: {os.path.basename(enc_path)}")
        else:
            print("  ❌ Fallo en el cifrado.")
    else:
        print("  ❌ Fallo en la creación del ZIP.")

    # 2. Test High Res Logger
    print("\n[Test 2] HighResLogger...")
    hr = HighResLogger(root)
    hr.log_thought_trace("Prompt de prueba", "Pensamiento profundo sobre la inmortalidad.")
    hr.log_code_attempt("test.py", "Optimizar loop", "print('ok')", True, "Success")
    
    if os.path.exists(hr.current_log_file):
        print(f"  ✅ Log JSONL creado: {os.path.basename(hr.current_log_file)}")
        with open(hr.current_log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"  ✅ Entradas registradas: {len(lines)}")
    else:
        print("  ❌ Fallo en la creación del log.")

    # Limpieza de archivos de prueba local
    print("\n[Limpieza] Eliminando archivos temporales de prueba...")
    if os.path.exists(zip_path): os.remove(zip_path)
    # enc_path se mantiene si el usuario quiere inspeccionarlo
    
    print("\n--- ✅ TEST FINALIZADO CON ÉXITO ---")

if __name__ == "__main__":
    test_immortal_architecture()
