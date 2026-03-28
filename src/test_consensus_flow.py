import os
import sys
import time
import logging

# Root path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.swarm.infrastructure_connector import InfrastructureConnector

def test_consensus():
    logging.basicConfig(level=logging.INFO)
    print("--- INICIANDO TEST DE CONSENSO DE INFRAESTRUCTURA ---")
    
    root = os.path.dirname(os.path.abspath(__file__))
    infra = InfrastructureConnector(root)
    
    print("\n[Test] Solicitando provisión de un nuevo nodo RTX4090...")
    print("[Test] (Esto debería disparar el GridConsensusProtocol y contactar a los satélites 8081/8082)")
    
    # Asegurar que haya presupuesto si no existe el wallet
    wallet_path = os.path.join(root, "agents", "swarm", "wallet.json")
    if not os.path.exists(wallet_path):
        import json
        with open(wallet_path, "w") as f:
            json.dump({"balance_usd": 100.0}, f)
            
    res = infra.provision_node("RunPod", "RTX4090")
    
    if res.get("success"):
        print("\n✅ ÉXITO: El nodo fue provisionado tras alcanzar el consenso.")
        print(f"ID del Nodo: {res['node_id']}")
    else:
        print(f"\n❌ FALLO: {res.get('error')}")

if __name__ == "__main__":
    test_consensus()
