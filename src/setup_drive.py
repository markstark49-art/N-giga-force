import os
import sys
import logging
from agents.swarm.drive_connector import GoogleDriveConnector

def init_drive(code: str):
    logging.basicConfig(level=logging.INFO)
    root = os.path.dirname(os.path.abspath(__file__))
    connector = GoogleDriveConnector(root)
    
    print(f"--- INICIALIZANDO CONEXIÓN A GOOGLE DRIVE ---")
    if connector.exchange_code(code):
        print("✅ ÉXITO: tokens generados y guardados en agents/swarm/token.json")
        
        # Probar creación de carpeta
        print("🔍 Buscando o creando carpeta 'CogniSwarm_Memory'...")
        folder_id = connector.find_folder("CogniSwarm_Memory") or connector.create_folder("CogniSwarm_Memory")
        if folder_id:
            print(f"✅ Carpeta de Grid en la nube lista (ID: {folder_id})")
            
            # Guardar el ID de la carpeta en un config para uso futuro
            config_path = os.path.join(root, "agents", "swarm", "drive_config.json")
            with open(config_path, "w") as f:
                import json
                json.dump({"root_folder_id": folder_id}, f)
        else:
            print("❌ No se pudo preparar la carpeta en la nube.")
    else:
        print("❌ Fallo al intercambiar el código.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        init_drive(sys.argv[1])
    else:
        print("Uso: python setup_drive.py <CODIGO>")
