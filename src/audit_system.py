"""
🔍 Cogni Swarm Global Health Check — Auditoría de Integridad
"""
import os
import sys
import ast
import traceback

def audit_files():
    print("--- 🔍 INICIANDO AUDITORÍA GLOBAL DE COGNI SWARM ---")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    exclude_dirs = {".git", "venv", ".evolution_backups", "tmp", "__pycache__"}
    
    errors_found = 0
    checked_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".py"):
                checked_count += 1
                f_path = os.path.join(root, file)
                try:
                    with open(f_path, "r", encoding="utf-8") as f:
                        source = f.read()
                    ast.parse(source)
                except SyntaxError as e:
                    print(f"❌ ERROR SINTAXIS en `{file}`: {e}")
                    errors_found += 1
                except Exception as e:
                    print(f"⚠️ ERROR LECTURA en `{file}`: {e}")
                    errors_found += 1

    print(f"\n--- RESUMEN AUDITORÍA ---")
    print(f"Archivos analizados: {checked_count}")
    print(f"Errores críticos: {errors_found}")
    
    if errors_found == 0:
        print("✅ Estructura sintáctica INTEGRAL.")
    else:
        print("🛑 Se requieren correcciones manuales.")

if __name__ == "__main__":
    audit_files()
