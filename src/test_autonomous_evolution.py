import sys
import os
import time

# Root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Forzar un ciclo de evolución en el autonomy_loop
os.environ["FORCE_EVOLUTION"] = "true"

from agents.autonomy_loop import run_autonomy_loop

if __name__ == "__main__":
    # Ejecutamos 1 ciclo (intervalo 0 para que sea inmediato y salga)
    # Necesitamos modificar el loop para que pueda salir o solo correr una vez para tests
    print("--- 🧪 TEST DE INTEGRACIÓN: EVOLUCIÓN AUTÓNOMA ---")
    # Para efectos del test, solo queremos ver si el código de evolución se ejecuta.
    # Como el loop es un 'while True', vamos a importar y llamar a la lógica interna directamente
    # o simplemente dejar que corra un poco.
    
    # Run loop with 0.01 interval (approx immediate)
    run_autonomy_loop(0.01)
