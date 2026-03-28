import os
import json
import time
import random

def simulate_activity(root_dir):
    wallet_path = os.path.join(root_dir, "agents", "swarm", "wallet.json")
    signals_path = os.path.join(root_dir, "agents", "swarm", "signals.json")
    
    print("[+] Simulador de Actividad Cogni-Swarm Iniciado...")
    
    # 1. Inyectar Balance
    wallet_data = {
        "balance_usd": 1250.75,
        "spent_today_usd": 12.45,
        "tokens_remaining": 8500000
    }
    with open(wallet_path, "w") as f:
        json.dump(wallet_data, f, indent=4)
    print("[OK] Wallet Simulada.")

    # 2. Inyectar Se?ales de Alta Carga
    signals_data = {
        "timestamp": time.time(),
        "components": {
            "KERNEL_MODULE": {"state": "MUTATING", "health": 0.4},
            "SINGULARITY_ENGINE_MODULE": {"state": "EVOLVING", "health": 0.5},
            "INFRA_MODULE": {"state": "PROVISIONING", "health": 0.9},
            "ORACLE_MODULE": {"state": "AWAITING_ORACLE", "health": 1.0}
        }
    }
    with open(signals_path, "w") as f:
        json.dump(signals_data, f, indent=4)
    print("[OK] Se?ales de Alta Carga Inyectadas.")

    print("\n[VERIFICACI?N]:")
    print("- Abre el HUD y revisa el balance: $1250.75")
    print("- Revisa las alertas en el Log T?ctico para recomendaciones de infraestructura.")
    print("- Observa los pings en el mapa de RED.")

if __name__ == "__main__":
    simulate_activity(".")
