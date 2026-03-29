import pandas as pd
import numpy as np

df = pd.read_csv('benchmark_soberania_v20.9.csv')

print("=== AUDITORÍA ESTADÍSTICA DEL DATASET ===")
print(df.describe().to_string())

print("\n=== VARIANZA POR COLUMNA ===")
for col in df.columns:
    v = df[col].var()
    estado = "✅ VÁLIDA" if v > 1e-20 else "❌ TRIVIAL"
    print(f"  {col}: {v:.4e} → {estado}")

print("\n=== CORRELACIÓN (para detectar señal real) ===")
corr = df[['paso','ruido','caos_total','entropia_promedio','chi_promedio']].corr()
print(corr.to_string())

print("\n=== VEREDICTO ===")
var_caos = df['caos_total'].var()
if var_caos < 1e-20:
    print("🚨 caos_total es prácticamente constante.")
    print("   PySR alucinó: ajustó una ecuación compleja sobre ruido numérico.")
    print("   VARIABLE TARGET: usar entropia_promedio en su lugar.")
else:
    print("✅ caos_total tiene varianza suficiente. PySR trabajó con señal real.")
