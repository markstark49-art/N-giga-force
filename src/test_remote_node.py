import os
import sys
import requests
from agents.swarm.satellite_manager import SatelliteManager

def test_remote_node():
    root = os.path.dirname(os.path.abspath(__file__))
    mgr = SatelliteManager(root)
    
    print("🔍 Escaneando satélites del Grid...")
    nodes = mgr.get_available_nodes()
    
    for node in nodes:
        url = node.get("url")
        node_id = node.get("node_id", "Unknown")
        print(f"📡 Nodo Detectado: {node_id} en {url}")
        
    remote_nodes = [n for n in nodes if "ngrok-free.dev" in n.get("url", "") or ".hf.space" in n.get("url", "")]
    if remote_nodes:
        print(f"\n✅ ÉXITO: Se detectaron {len(remote_nodes)} satélites remotos activos.")
        for node in remote_nodes:
            print(f"Propiedades [{node.get('url')}]: {node}")
    else:
        print("\n❌ FALLO: No se detectaron satélites remotos activos. Revisa los túneles y visibilidad.")

if __name__ == "__main__":
    test_remote_node()
