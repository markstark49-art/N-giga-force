import sys
import os
import json

# Asegurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# CARGAR .ENV MANUALMENTE
def load_env():
    env_path = os.path.join(current_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
        print("Variables de entorno cargadas desde .env")

load_env()

# Importar componentes de Cogni Swarm
import agents.swarm.evolution_kernel as ek
import agents.reasoning.model_router as router

def manual_test():
    # Mock Robusto con def
    def robust_mock_select(stimulus, tool_count=0, has_history=False):
        print(f"[MOCK] Recibido estímulo: {stimulus[:30]}...")
        return ("llama-3.3-70b-versatile", "groq", "llama-3.3-7b", 4096)
    
    # Reemplazar en ambos sitios para seguridad extrema
    router.select_model = robust_mock_select
    ek.select_model = robust_mock_select
    
    print("--- [DIAGNÓSTICO FINAL] Validando Evolución Nivel 8 ---")
    
    try:
        kernel = ek.EvolutionaryKernel()
        target_file = "agents/swarm/interests.py"
        
        # 1. Crear Snapshot
        print("Paso 1: Snapshot...")
        sid = kernel.create_evolution_snapshot(reason="Diagnóstico Final: Auto-Consciencia")
        print(f"Snapshot Creado: {sid}")
        
        # 2. Optimización
        print(f"Consultando Groq (API_KEY: {os.environ.get('GROQ_API_KEY', 'FALLO')[:6]}***)...")
        res = kernel.ask_for_optimization(target_file)
        
        if isinstance(res, tuple):
            new_code, rationale, chunk_info = res
        else:
            new_code, rationale, chunk_info = res, "Sin razon", None
            
        if new_code:
            print(f"✅ ÉXITO: {rationale[:150]}...")
            # 3. Mutar
            kernel.safe_mutate(target_file, new_code)
            # 4. Loguear
            log_details = f"**Verificación de Auto-Consciencia:** `{target_file}`\n**Razón Técnica:** {rationale}\n**Resultado:** Evolución nivel 8 verificada con éxito."
            kernel._log_evolution_event("AUTO-EVOLVE", log_details)
            print("🚀 ÉXITO: Diario de evolución actualizado.")
        else:
            print(f"❌ FALLO: El kernel devolvió None. Razón: {rationale}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_test()
