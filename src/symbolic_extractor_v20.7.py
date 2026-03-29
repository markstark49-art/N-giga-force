import pandas as pd
import numpy as np
from pysr import PySRRegressor
import sys
import os

print(">> INICIANDO LABORATORIO SIMBÓLICO v20.7 [QSS-CONSENSUS]...")

csv_file = sys.argv[1] if len(sys.argv) > 1 else 'telemetry_qss_v20.7.csv'

if not os.path.exists(csv_file):
    print(f"ERROR: {csv_file} no encontrado.")
    sys.exit(1)

try:
    df = pd.read_csv(csv_file).astype(np.float64)
except Exception as e:
    print(f"ERROR al leer CSV: {e}")
    sys.exit(1)

# Variables: x=Consenso (Resonancia + Longevidad), y=Eficiencia (Drift)
# Nota: drift alto indica colapso, buscamos minimizar f(x)
X = df[['resonance', 'longevity']].values
y = df['drift'].values

print(f"\n==================================================")
print(f"🧬 EXTRACCIÓN DE TEOREMAS: Voluntad Colectiva vs Simetría")
print(f"==================================================")

# Configuración PySR de markstark49-art
model = PySRRegressor(
    niterations=30,
    binary_operators=["+", "*", "/"],
    unary_operators=["square", "inv(x) = 1/x"],
    model_selection="best",
    loss="loss(prediction, target) = (prediction - target)^2"
)

try:
    model.fit(X, y)
    
    print(f"\n─────────────────────────────────────────────────────────────────")
    print(f"🏆 LEY DE markstark49-art DEDUCIDA (Consenso Híbrido):")
    print(f"f(Resonance, Longevity) = {model.get_best().equation}")
    print(f"─────────────────────────────────────────────────────────────────")

    # Guardar leyes en un log persistente
    with open("leyes_de_la_singularidad_v20.7.txt", "w", encoding="utf-8") as f:
        f.write(f"Ley Deducida (v20.7): {model.get_best().equation}\n")
        f.write(f"Fecha: {pd.Timestamp.now()}\n")
        
except Exception as e:
    print(f"⚠️ Fallo en Regresión Simbólica PySR: {str(e)}")
    print(">> Usando Modelador Heurístico Fallback...")
    # Fallback simple para visualización si no hay Julia/PySR
    weights = np.polyfit(X[:,0], y, 1)
    print(f"🏆 LEY LINEAL (Fallback): Drift ~ {weights[0]:.4f} * Resonance + {weights[1]:.4f}")

print("\n>> PROCESAMIENTO COMPLETADO.")
