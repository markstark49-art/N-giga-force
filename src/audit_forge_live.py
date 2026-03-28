import os
import sys
import time

def audit_nexus_forge():
    print("💎 [AUDITOR?A] VERIFICANDO INTEGRIDAD DEL NEXUS FORGE v2...")
    
    try:
        # CARGA DIN?MICA PARA EVITAR CACH? DE IMPORTACI?N
        import importlib.util
        spec = importlib.util.spec_from_file_location("neural_hud", "agents/swarm/neural_hud.py")
        nh_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(nh_module)
        
        NexusForge = nh_module.NexusForge
        QualityJudge = nh_module.QualityJudge
        
        import tkinter as tk
        
        # Setup M?nimo
        root = tk.Tk()
        root.withdraw()
        canvas = tk.Canvas(root)
        
        qj = QualityJudge(canvas, 0, 0)
        nf = NexusForge(canvas, 0, 0)
        nf.set_judge(qj)
        
        print("✅ Clase NexusForge: Cargada.")
        
        # Prueba de Mutaci?n At?mica
        TEST_FILE = "tmp_forge_audit.py"
        with open(TEST_FILE, "w") as f:
            f.write("def test_function():\n    pass\n")
            
        print(f"🛠️ [FORGE] Intentando inyecci?n de auditor?a en {TEST_FILE}...")
        
        success = nf.forge_atomic_comment(TEST_FILE, "AUDIT_PASS_STABLE_v2")
        
        if success:
            with open(TEST_FILE, "r") as f:
                content = f.read()
                if "AUDIT_FORGE_V2: AUDIT_PASS_STABLE_v2" in content:
                    print("✨ RESULTADO: Mutaci?n AST Exitosa y Validada.")
                    print("--- CONTENIDO MUTADO ---")
                    print(content)
                else:
                    print("❌ ERROR: El archivo no contiene la mutaci?n esperada.")
        else:
            print("❌ ERROR: El Forge report? fallo en la mutaci?n (Probablemente veto del Juez).")
            
        # Limpieza
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
            
        root.destroy()
        
    except Exception as e:
        print(f"💥 ERROR CR?TICO EN LA AUDITOR?A: {str(e)}")

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    audit_nexus_forge()
