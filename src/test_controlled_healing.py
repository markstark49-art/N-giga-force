import os
import time
import tkinter as tk
from agents.swarm.neural_hud import NeuralHUD

def run_controlled_healing_test():
    print("🛡️ [TEST] INICIANDO PRUEBA DE INMUNIDAD SIST?MICA...")
    
    # 1. Instanciamos el HUD (modo headless si es posible, o normal para ver)
    # Para la prueba, usaremos los componentes internos directamente
    app = NeuralHUD()
    
    # 2. Simulamos una "Infecci?n" (Error de L?gica)
    # Supongamos que la funci?n 'update' de UMLClassNode sufri? una anomal?a
    target_file = "agents/swarm/neural_hud.py"
    target_func = "update"
    error_msg = "DivisionByZero in health calculation (simulated)"
    
    print(f"🦠 [INFECT] Simulando error en: {target_func}")
    
    # 3. El Sistema Inmune detecta el error y ordena la reparaci?n
    success = app.immune_system.report_logic_error(target_file, target_func, error_msg)
    
    if success:
        print("\n✨ [HEALED] ¡EL SISTEMA SE HA AUTOREPARADO!")
        print(f"   El Forge inyect? un parche de seguridad en {target_file}")
        print(f"   Curaciones totales en este ciclo: {app.immune_system.repaired_count}")
        
        # 4. Verificamos la inyecci?n (opcional, leyendo el archivo)
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
            if "⚠️ SELF-HEALED" in content:
                print("\n✅ VERIFICACI?N ESTRUCTURAL: El parche est? presente en el ADN.")
            else:
                print("\n❌ VERIFICACI?N FALLIDA: El parche no se encuentra.")
    else:
        print("\n💀 [FAIL] El Sistema Inmune no pudo contener la infecci?n.")

    app.destroy()

if __name__ == "__main__":
    run_controlled_healing_test()
