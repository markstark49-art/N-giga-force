import os
import sys
import json
import time

# Añadir raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.swarm.satellite_manager import SatelliteManager
from agents.swarm.groq_limiter import GroqRateLimiter

def test_distributed_synthesis():
    print("--- INICIANDO TEST DE SÍNTESIS DISTRIBUIDA ---")
    root = os.path.dirname(os.path.abspath(__file__))
    mgr = SatelliteManager(root)
    
    # 1. Verificar nodos activos
    nodes = mgr.get_available_nodes()
    print(f"Nodos detectados: {len(nodes)}")
    if not nodes:
        print("❌ Error: No hay nodos satélite activos (8081/8082).")
        return

    # 2. Probar delegación directa
    prompt = "Explica brevemente qué es un enjambre de LLMs."
    print(f"Enviando prompt al satélite: '{prompt}'")
    
    response = mgr.delegate_synthesis(prompt, system_prompt="Eres un experto en inteligencia artificial colectiva.")
    
    if response:
        print(f"✅ Respuesta recibida del satélite:\n---\n{response}\n---")
    else:
        print("❌ Fallo en la respuesta del satélite.")

    # 3. Probar integración con GroqLimiter (Si es posible simular throttling)
    print("\n--- TEST DE INTEGRACIÓN CON GROQLIMITER ---")
    limiter = GroqRateLimiter.get_instance()
    
    # Verificamos si podemos obtener una respuesta de error del satélite directamente
    node = nodes[0]
    url = node["url"]
    print(f"Probando endpoint /synthesis directamente en {url}...")
    try:
        from agents.swarm.swarm_security import SwarmSecurity
        sec = SwarmSecurity(root)
        payload = {"prompt": "Hola", "system_prompt": "Test"}
        enc = sec.encrypt_payload(payload)
        header = {"Authorization": f"Bearer {sec.generate_token('test')}"}
        import requests
        r = requests.post(f"{url}/synthesis", json={"payload": enc}, headers=header, timeout=10)
        print(f"Status Satélite: {r.status_code}")
        if r.status_code == 200:
            dec = sec.decrypt_payload(r.json().get("payload"))
            print(f"Decrypted Res: {dec}")
        else:
            print(f"Error Raw: {r.text}")
    except Exception as e:
        print(f"Error en request directa: {e}")

if __name__ == "__main__":
    test_distributed_synthesis()
