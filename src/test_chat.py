import os
from dotenv import load_dotenv
from agents.reasoning.generation import TextGenerator

load_dotenv()

# Only run if GROQ_API_KEY is present
if not os.getenv("GROQ_API_KEY"):
    print("Please set GROQ_API_KEY environment variable before running.")
    exit(1)

# Initialize only the text generator to bypass heavy vision models
print("Iniciando solo el Motor Generativo (TextGenerator)...")
agent = TextGenerator()

session = "test_session_mcp"

# Simple conversation to test the UI generator streaming
messages = [
    "Usa tu orquestador para ejecutar `dir` y dime cuántos archivos y carpetas ves."
]

for msg in messages:
    print(f"\nUsuario: {msg}")
    
    # We pass empty memory lists because we are bypassing SimEnv cache
    generator = agent.generate_response(msg, [], [])
    
    for chunk in generator:
        if chunk["type"] == "step":
            print(f"🔄 {chunk['content']}")
        elif chunk["type"] == "final":
            print(f"\n✅ REPSUESTA FINAL:\n{chunk['content']}\n")
        elif chunk["type"] == "error":
            print(f"❌ ERROR: {chunk['content']}")

# The TextGenerator does not have a cache in the same way SimEnv does,
# so this section for printing cache history is no longer applicable.
# print("\n--- Historial en Cache ---")
# for m in env.cache.get_history(session):
#     print(f"{m['role'].capitalize()}: {m['content'][:50]}...")
