import os
import sys
import json
from datetime import datetime
from agents.swarm.concept_mapper import ConceptMapper
from agents.swarm.high_res_logger import HighResLogger

def test_concept_mapping():
    root = os.getcwd()
    print("--- 🧠 INICIANDO TEST DE MAPEO CONCEPTUAL ---")
    
    # 1. Preparar logs de prueba
    logger = HighResLogger(root)
    log_date = datetime.now().strftime("%Y%m%d")
    print(f"  [Setup] Generando logs de prueba para {log_date}...")
    
    logger.log_thought_trace("Iniciando Phase 120", "Estamos expandiendo a 2 TB de memoria.")
    logger.log_code_attempt("snapshot_manager.py", "Crear backup", "zip()", True)
    
    # 2. Ejecutar Mapper
    print("\n[Test] ConceptMapper.generate_map()...")
    mapper = ConceptMapper(root)
    # Por seguridad en el test, simulamos una respuesta de Mermaid si no hay API key real
    # Pero aquí intentaremos la ejecución real si es posible.
    report_path = mapper.generate_map(log_date)
    
    if report_path and os.path.exists(report_path):
        print(f"  ✅ Reporte generado: {os.path.basename(report_path)}")
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "graph TD" in content or "mermaid" in content:
                print("  ✅ Estructura Mermaid detectada.")
            else:
                print("  ⚠️ El reporte no parece contener un grafo válido.")
    else:
        print("  ❌ Fallo en la generación del mapa.")

    print("\n--- ✅ TEST FINALIZADO ---")

if __name__ == "__main__":
    test_concept_mapping()
