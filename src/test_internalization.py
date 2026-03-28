import sys
import os

# Root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.sim_environment import SimEnv

def test_internalization():
    print("--- Test de Internalización de Conocimiento ---")
    env = SimEnv()
    
    test_text = """
    ## TEMA: Avances en Computación Cuántica 2026
    Los procesadores de 10,000 qubits ya son una realidad estable gracias al enfriamiento por láser ionizado.
    Esto permite romper el cifrado RSA en segundos.
    """
    
    print("Simulando guardado de reporte autónomo...")
    result = env.learn_from_text(test_text, source_name="Test de Autonomía")
    
    if result.get('stored'):
        print(f"✅ ÉXITO: Conocimiento guardado. Palabras procesadas: {result.get('words_processed')}")
    else:
        print("❌ FALLO: No se pudo guardar el conocimiento en Pinecone.")

if __name__ == "__main__":
    test_internalization()
