import time
import random

def run_rl_loop():
    print("Iniciando Reinforcement Learning Loop...")
    while True:
        reward = random.random()
        print(f"Iteración completada. Recompensa: {reward:.4f}")
        time.sleep(10)

if __name__ == "__main__":
    run_rl_loop()
