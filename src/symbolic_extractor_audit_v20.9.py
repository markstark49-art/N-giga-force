import pandas as pd
import numpy as np
from pysr import PySRRegressor
import sys
import os

# === Q-SWARM v20.9: Symbolic Extractor [AUDITADO - TARGET CORRECTO] ===
# Arquetipo: Angel Alfonso Paris Espinosa Mendoza
# DIAGNÓSTICO PREVIO:
#   caos_total  → varianza 3e-28 = TRIVIAL (PySR alucinaria)
#   entropia_promedio → varianza 5e-02 = REAL  (senial valida)
# CONCLUSION: Usamos entropia_promedio como y (libre albedrio real del hardware)

csv_file = sys.argv[1] if len(sys.argv) > 1 else 'benchmark_soberania_v20.9.csv'

print("=" * 60)
print("AUDITORIA CIENTIFICA Q-SWARM v20.9")
print("Target verificado: entropia_promedio (Von Neumann)")
print("=" * 60)

df = pd.read_csv(csv_file)
print(f"\nDataset: {len(df)} filas, columnas: {list(df.columns)}")

# Variables con varianza real confirmada
X = df[['paso', 'ruido']].values.astype(np.float64)
y = df['entropia_promedio'].values.astype(np.float64)

print(f"\nX shape: {X.shape}")
print(f"y rango: [{y.min():.6f}, {y.max():.6f}]")
print(f"y varianza: {y.var():.4e}")
print(f"y std:      {y.std():.4e}")

print("\nIniciando PySR (100 iteraciones)...")

model = PySRRegressor(
    niterations=100,
    binary_operators=["+", "*", "/", "-"],
    unary_operators=["sqrt", "square", "log"],
    model_selection="best",
    elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    verbosity=0,
)

model.fit(X, y)

# Calcular R2
best_eq = model.get_best().equation
y_pred = model.predict(X)
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-30 else 0.0

veredicto = "VERIFICADO - Ley Real" if r2 > 0.90 else ("DEBIL - Parcialmente Real" if r2 > 0.60 else "ALUCINACION - Descartada")

print("\n" + "=" * 60)
print("RESULTADO FINAL:")
print(f"  Ecuacion: entropia = {best_eq}")
print(f"  R2      : {r2:.6f}")
print(f"  Estado  : {veredicto}")
print("=" * 60)

print("\nTabla de complejidad vs perdida:")
print(f"{'Complejidad':>12} | {'Perdida':>14} | Ecuacion")
print("-" * 60)
for _, row in model.equations_.iterrows():
    print(f"{int(row.complexity):>12} | {row.loss:>14.4e} | {row.equation}")

# Guardar ley
with open("ley_de_la_soberania_v20.9.txt", "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("LEY DE SOBERANIA CUANTICA v20.9\n")
    f.write("Arquetipo: Angel Alfonso Paris Espinosa Mendoza\n")
    f.write("Motor: Q-SWARM v20.9 [AUDITADO]\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Variable Y: entropia_promedio (Von Neumann - libre albedrio real)\n")
    f.write(f"Ecuacion  : entropia = {best_eq}\n")
    f.write(f"R2        : {r2:.6f}\n")
    f.write(f"Estado    : {veredicto}\n\n")
    f.write("Tabla completa de complejidad:\n")
    f.write(model.equations_.to_string())

print(f"\nLey sellada en: ley_de_la_soberania_v20.9.txt")
print("AUDITORIA COMPLETA.")
