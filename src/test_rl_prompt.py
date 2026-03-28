import os
import sys

root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root)

from agents.swarm.evolution_kernel import EvolutionaryKernel

def mock_call_groq(prompt, system_prompt="Eres un optimizador de código.", model=None, provider=None):
    print("\n" + "="*50)
    print("PROMPT EVALUADO:")
    print("="*50)
    print(prompt)
    print("="*50)
    return "[OPTIMIZED_CODE]\n```python\n# ok\n```\n[/OPTIMIZED_CODE]"

def test_rl_injection():
    kernel = EvolutionaryKernel(root)
    # Sobrescribir temporalmente la función que llama a LLM para solo ver el prompt
    kernel._call_groq = mock_call_groq
    
    # Simular una petición de optimización
    print("📝 Testeando ask_for_optimization...")
    # Usar un archivo de prueba arbitrario
    # Usar el propio test como dummy file
    test_file = os.path.join(root, "test_rl_prompt.py")
    kernel.ask_for_optimization(test_file)

if __name__ == "__main__":
    test_rl_injection()
