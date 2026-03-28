import os
import sys
import json

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.sim_environment import SimEnv

def test_interaction():
    print("Testing 'hola' interaction...")
    env = SimEnv()
    try:
        for chunk in env.run_step(stimulus_text="Hola, ¿cómo estás?", session_id="test_session"):
            print(f"Chunk: {chunk}")
        print("Interaction finished successfully.")
    except Exception as e:
        print(f"Error during interaction: {e}")

if __name__ == "__main__":
    test_interaction()
