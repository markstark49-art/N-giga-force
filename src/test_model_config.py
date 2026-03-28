import sys
import os
import requests

# Añadir el path del proyecto
sys.path.append(os.getcwd())

from agents.reasoning.model_router import select_model

def test_router():
    print("--- Probando Enrutador de Modelos ---")
    model, provider, fallback, ctx = select_model("hola, ¿quién eres?")
    print(f"Estímulo: 'hola'")
    print(f"Modelo seleccionado: {model} (Esperado: llama3.2:3b)")
    print(f"Proveedor: {provider}")
    
    if model == "llama3.2:3b":
        print("✅ TEST PASADO: El enrutador apunta al nuevo modelo de la GPU.")
    else:
        print("❌ TEST FALLIDO: El enrutador no está configurado correctamente.")

def test_ollama_connectivity():
    print("\n--- Probando Conectividad con Ollama Local ---")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    try:
        response = requests.get(f"{url}/api/tags")
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            print(f"Modelos detectados en Ollama: {models}")
            if "llama3.2:3b" in models or "llama3.2:latest" in models:
                print("✅ TEST PASADO: llama3.2 está disponible en Ollama.")
            else:
                print("⚠️ ADVERTENCIA: llama3.2:3b no se encontró en la lista. ¿Ya hiciste 'ollama pull llama3.2:3b'?")
        else:
            print(f"❌ ERROR: Ollama respondió con status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: No se pudo conectar con Ollama en {url}. Asegúrate de que Ollama esté corriendo.")

if __name__ == "__main__":
    test_router()
    test_ollama_connectivity()
