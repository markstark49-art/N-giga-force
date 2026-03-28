import os
import time
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(root_dir, "evolution_history.md")

def inject_event(event_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"## [{timestamp}] {event_type}\n{details}\n\n"
    with open(log_path, "a", encoding="latin-1") as f:
        f.write(entry)
    print(f"[TEST] Inyectado: {event_type}")

print("--- 🧪 INICIANDO PRUEBA DE STREAMING REAL-TIME ---")
print("Observa la pestaña [EVOLUCION] en tu HUD...")

# Evento 1: Snapshot
inject_event("SNAPSHOT", "Snapshot de seguridad `test-sync-001` creado antes de la prueba de fuego.")
time.sleep(2)

# Evento 2: Mutación
inject_event("MUTATION", "Aplicando optimización de latencia en `agents/swarm/neural_hud.py` (Simulación de prueba).")
time.sleep(2)

# Evento 3: Fitness
inject_event("FITNESS", "Evaluación de Aptitud: **Score 195.50**\n- Mejora de renderizado detectada: +15%.")
time.sleep(2)

print("--- ✅ PRUEBA COMPLETADA ---")
