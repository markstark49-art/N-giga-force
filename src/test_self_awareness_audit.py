import os
import sys

# Agregar raiz al path
root = os.getcwd()
sys.path.append(root)

from agents.swarm.architecture_mirror import ArchitectureMirror

def test_self_awareness():
    print("--- 🧠 PRUEBA DE AUTOCONSCIENCIA ESTRUCTURAL (FASE 160) ---")
    mirror = ArchitectureMirror(root)
    
    # 1. Probar escaneo
    status = mirror.scan_vault()
    print(f"[TEST 1] {status}")
    if len(mirror.index) == 0:
        print("[FAIL] La boveda esta vacia o no se pudo indexar.")
        return

    # 2. Probar extraccion de contexto semantico
    target = "drive_connector.py"
    print(f"\n[TEST 2] Solicitando contexto para: {target}")
    context = mirror.get_context_for_file(target)
    
    if "RELEVANT BLUEPRINT" in context:
        print(f"[SUCCESS] Se encontro contexto relevante ({len(context)} caracteres).")
        # Mostrar fragmento
        print("\nFragmento de plano maestro inyectado:")
        print("-" * 30)
        print(context[:300] + "...")
        print("-" * 30)
    else:
        print("[WARNING] No se encontro contexto especifico para 'drive_connector', pero el motor funciona.")

    # 3. Probar ARCHITECTURE_MASTER
    if os.path.exists(mirror.master_file):
        print("\n[TEST 3] ARCHITECTURE_MASTER detectado. Integridad OK.")
    else:
        print("\n[FAIL] ARCHITECTURE_MASTER no encontrado en la raiz.")

if __name__ == "__main__":
    test_self_awareness()
