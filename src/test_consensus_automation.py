"""
🧪 Test Consenso y Auto-Escalado — Validación Nivel 16+
"""
import os
import sys
import asyncio
import json

# Añadir raíz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.swarm.grid_consensus import GridConsensus
from agents.swarm.infrastructure_connector import InfrastructureConnector
from agents.swarm.economic_agent import EconomicAgent

async def test_consensus_flow():
    print("--- 🗳️ TEST DE CONSENSO DE REJILLA ---")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    consensus = GridConsensus(root_dir)
    
    # 1. Verificar lectura de satélites
    satellites = consensus._get_active_satellites()
    print(f"Satélites detectados: {len(satellites)}")
    
    # 2. Ejecutar ciclo de consenso
    # Nota: Esto fallará si los nodos no están encendidos, pero validamos el flujo
    print("\nIniciando votación para UPDATE_KERNEL...")
    # Bajamos el min_votes a 1 para que el voto del cerebro central baste en el test
    success = await consensus.run_consensus("TEST_ACTION", "Detalles de prueba", min_votes=1)
    print(f"Soberanía alcanzada: {success}")

def test_autoscaling_logic():
    print("\n--- 🚀 TEST DE LÓGICA DE AUTO-ESCALADO ---")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    infra = InfrastructureConnector(root_dir)
    econ = EconomicAgent(root_dir)
    
    # Simular saldo suficiente
    wallet = econ.load_wallet()
    balance = wallet.get("balance_credits", 0)
    print(f"Saldo actual: {balance} cr")
    
    if balance >= 1500:
        print("Saldo suficiente para escalado. Simulando aprovisionamiento...")
        success = infra.provision_node(node_type="RTX_4090_TEST")
        if success:
            print("✅ Escalado exitoso en el simulador.")
    else:
        print("Saldo insuficiente (esperado si la wallet está vacía).")

if __name__ == "__main__":
    asyncio.run(test_consensus_flow())
    test_autoscaling_logic()
