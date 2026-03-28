import sys
import os

# Root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.swarm.evolution_kernel import EvolutionaryKernel

def test_evolution_safety():
    kernel = EvolutionaryKernel()
    
    print("--- TEST 1: Snapshot Somático ---")
    sid = kernel.create_evolution_snapshot()
    if sid:
        print(f"PASS: Snapshot {sid} creado.")
    else:
        print("FAIL: No se pudo crear el snapshot.")
        return

    print("\n--- TEST 2: Protección del Guardian ---")
    protected_file = "agents/reasoning/guardian.py"
    print(f"Intentando mutar {protected_file}...")
    success = kernel.safe_mutate(protected_file, "print('hackeado')")
    if not success:
        print("PASS: Guardian bloqueó la mutación del núcleo ético.")
    else:
        print("FAIL: Guardian permitió mutar un archivo protegido.")

    print("\n--- TEST 3: Mutación Permitida ---")
    safe_file = "hola_mundo.py"
    success = kernel.safe_mutate(safe_file, "print('Hola Evolucionado')")
    if success:
        print(f"PASS: Mutación permitida en {safe_file}.")
    else:
        print(f"FAIL: No se pudo mutar un archivo seguro.")

    print("\n--- TEST 4: Rollback ---")
    if kernel.rollback_to_snapshot(sid):
        print(f"PASS: Rollback al estado inicial exitoso.")
    else:
        print("FAIL: Falló el rollback.")

if __name__ == "__main__":
    test_evolution_safety()
