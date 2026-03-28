import sys
import os
import json

# Adjust path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from agents.swarm.thought_bucket import ThoughtBucketManager
    
    print("Iniciando Prueba de Telepatía P2P...")
    bucket = ThoughtBucketManager()
    
    nuevo_pensamiento = {
        "node_id": "Angel-Smartphone",
        "task": "Investigar arquitecturas de RAG multi-modal para la Fase 134",
        "priority": "alta"
    }
    
    bucket.drop_thought("Angel-Smartphone", nuevo_pensamiento)
    print("✅ Pensamiento inyectado en la bandeja de entrada P2P exitosamente.")
    
    # Comprobar que está ahí
    inbox = bucket.peek_inbox()
    print(f"Bandeja de entrada tiene {len(inbox)} pensamientos esperando.")
    
except Exception as e:
    print(f"❌ Error en la prueba: {e}")
