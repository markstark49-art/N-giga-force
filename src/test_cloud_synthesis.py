import os
from agents.swarm.satellite_manager import SatelliteManager

def test_final_synthesis():
    root = os.path.dirname(os.path.abspath(__file__))
    mgr = SatelliteManager(root)
    
    print("\n🚀 INICIANDO PRUEBA DE SÍNTESIS GLOBAL...")
    print("----------------------------------------")
    
    prompt = "¿Cómo ha evolucionado la arquitectura del enjambre al integrar satélites 24/7 en Hugging Face?"
    
    # Intentamos delegar. SatelliteManager elegirá el primer nodo disponible (habitualmente el remoto si lo pusimos al final o por orden).
    # Para forzar el satélite HF para esta prueba:
    hf_url = "https://cogniswarm-cogni-satellite-1.hf.space"
    
    print(f"📡 Delegando pensamiento a {hf_url}...")
    
    # Mocking the selection for the test
    response = mgr.delegate_synthesis(prompt, system_prompt="Eres un nodo de síntesis persistente de Cogni Swarm.")
    
    if response:
        print("\n🧠 RESPUESTA DEL ENJAMBRE (DIFUNDIDA):")
        print(f"'{response[:200]}...'")
        print("\n✅ ÉXITO: El tráfico de pensamientos ahora fluye a través de tu satélite permanente.")
    else:
        print("\n❌ FALLO: No se recibió respuesta del satélite. Revisa los logs de HF.")

if __name__ == "__main__":
    test_final_synthesis()
