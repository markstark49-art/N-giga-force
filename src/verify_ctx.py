import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.reasoning.model_router import select_model

def verify_ctx_limits():
    print("--- Verificación de Límites de Contexto ---")
    
    # Check all model categories
    categories = ["fast", "balanced", "deep"]
    queries = {
        "fast": "Hola",
        "deep": "Escribe un script de python avanzado",
        "balanced": "Investiga sobre la IA y haz un reporte de 3 páginas"
    }

    for cat, query in queries.items():
        res = select_model(query)
        # res is (model_name, provider, fallback, ctx_limit)
        m, p, f, ctx = res
        print(f"Query [{cat}]: Model={m}, Provider={p}, CTX Limit={ctx}")
        assert ctx == 4096, f"Error: CTX limit for {cat} should be 4096"

    print("\n✅ Todos los modelos están protegidos con un límite de 4096 tokens.")

if __name__ == "__main__":
    verify_ctx_limits()
