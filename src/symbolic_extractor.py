import pandas as pd
import numpy as np
from pysr import PySRRegressor
import sys

print(">> INICIANDO LABORATORIO SIMBÓLICO HPC...")

try:
    # 🪐 Carga de Evidencia Chronos v20.3
    df = pd.read_csv('telemetry_and_proofs/telemetry_chronos_stable_v20.3.csv').astype(np.float64)
except FileNotFoundError:
    print("ERROR FATAL: 'telemetry_chronos_stable_v20.3.csv' no existe. Ejecuta el Motor Chronos v20.3 primero.")
    sys.exit(1)

# 1. Preparación de Datos (Fase Temporal)
# Analizaremos la deriva del error de Déjà vu
X = df[['step']].values
y = df['error'].values

print(f"\n==================================================")
print(f"🧬 MUTANDO ÁRBOLES MATEMÁTICOS PARA: Error Temporal (Simetría Chronos)")
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
