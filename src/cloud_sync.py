import os
import sys
import json
import logging
from agents.swarm.drive_connector import GoogleDriveConnector

def cloud_sync():
    logging.basicConfig(level=logging.INFO)
    root = os.path.dirname(os.path.abspath(__file__))
    
    # Cargar ID de carpeta raíz
    config_path = os.path.join(root, "agents", "swarm", "drive_config.json")
    if not os.path.exists(config_path):
        print("❌ Drive no configurado. Ejecuta setup_drive.py primero.")
        return
        
    with open(config_path, "r") as f:
        config = json.load(f)
        folder_id = config.get("root_folder_id")

    connector = GoogleDriveConnector(root)
    
    # Directorio de artefactos (buscar el más reciente o el actual)
    # En este entorno, el brain dir está en la metadata
    brain_dir = os.path.join(os.environ["USERPROFILE"], ".gemini", "antigravity", "brain", "c828bab7-a509-4aed-9ffe-537eac83ccf1")
    
    files_to_sync = [
        os.path.join(root, "evolution_history.md"),
        os.path.join(root, "KERNEL_VERSIONS.md"),
        os.path.join(root, "DOCUMENTACION.md")
    ]
    
    # Añadir todos los .md del brain dir
    if os.path.exists(brain_dir):
        for f in os.listdir(brain_dir):
            if f.endswith(".md"):
                files_to_sync.append(os.path.join(brain_dir, f))

    print(f"--- INICIANDO CLOUD SYNC A FOLDER {folder_id} ---")
    for f_path in files_to_sync:
        if os.path.exists(f_path):
            print(f"⬆️ Subiendo {os.path.basename(f_path)}...")
            connector.upload_file(f_path, folder_id=folder_id)
        else:
            print(f"⚠️ Saltando {f_path} (No existe)")

    print("\n✅ CLOUD SYNC COMPLETADO.")

if __name__ == "__main__":
    cloud_sync()
