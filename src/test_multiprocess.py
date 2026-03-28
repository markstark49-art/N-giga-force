import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agents.swarm.swarm_orchestrator import SwarmOrchestrator

def main():
    orc = SwarmOrchestrator()
    print("Orchestrator initialized. Starting multiprocess test...")
    try:
        # Prompt forces planner to dispatch at least default agents
        for chunk in orc.run("Busca qué es el Bosón de Higgs y escribe un resumen de 2 líneas."):
            print("YIELD:", chunk)
    except Exception as e:
        print("Test failed with exception:", e)

if __name__ == '__main__':
    main()
