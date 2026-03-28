import pandas as pd
import numpy as np
from pysr import PySRRegressor
import sys

print(">> INICIANDO LABORATORIO SIMBÓLICO HPC...")

try:
    # 🪐 Carga de Evidencia Cuántica v19.0
    df = pd.read_csv('telemetry_and_proofs/telemetry_quantum_gravity_v19.0.csv').astype(np.float64)
except FileNotFoundError:
    print("ERROR FATAL: 'telemetry_quantum_gravity_v19.0.csv' no existe. Ejecuta el Motor v19.0 primero.")
    sys.exit(1)

# 1. Preparación de Datos (Fase Celeste Industrial)
# Analizaremos cómo la distancia a la Tierra escala la Energía Cinética
X = df[['avg_dist_earth']].values
y = df['kinetic_energy'].values

print(f"\n==================================================")
print(f"🧬 MUTANDO ÁRBOLES MATEMÁTICOS PARA: Vx (Eficiencia Geométrica)")
print(f"==================================================")

# 2. Configuración del Regresor Simbólico (PySR)
model = PySRRegressor(
    niterations=40,
    binary_operators=["+", "*", "/"],
    unary_operators=["square"], # Relación cuadrática esperada P ~ v^2 * R^2
    model_selection="best",
    loss="loss(prediction, target) = (prediction - target)^2"
)

# 3. Entrenamiento (Ejecución de Julia)
model.fit(X, y)

print(f"\n─────────────────────────────────────────────────────────────────")
print(f"🏆 LEY DE EFICIENCIA GEOMÉTRICA DEDUCIDA (Nuclear 2026):")
print(f"{model.get_best().equation}")
print(f"─────────────────────────────────────────────────────────────────")

print("\n>> EXTRACCIÓN COMPLETADA.")
