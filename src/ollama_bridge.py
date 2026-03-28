import requests
import json
import time

class OllamaBridge:
    def __init__(self, model="deepseek-gpu:latest", url="http://localhost:11434"):
        self.url = f"{url}/api/generate"
        self.model = model
        self.is_active = self._check_connection()

    def _check_connection(self):
        try:
            response = requests.get(self.url.replace("/generate", "/tags"), timeout=2)
            return response.status_code == 200
        except:
            return False

    def ask_coder(self, prompt: str, system_prompt: str = "Actúa como un experto en el lenguaje Verse de Fortnite (UEFN). Genera solo código puro."):
        if not self.is_active: return "ERROR: Ollama Link Inactivo."
        payload = {
            "model": self.model,
            "prompt": f"{system_prompt}\n\nUSER TASK: {prompt}",
            "stream": False,
            "options": {"temperature": 0.2, "num_gpu": 1}
        }
        print(f"[OllamaBridge] [QUERY] Enviando a {self.model}...")
        try:
            r = requests.post(self.url, json=payload)
            if r.status_code == 200:
                result = r.json().get('response', '')
                print(f"[OllamaBridge] [DONE] Recibido.")
                return result
            return f"ERROR: API Código {r.status_code}"
        except Exception as e:
            return f"ERROR: {str(e)}"

if __name__ == "__main__":
    bridge = OllamaBridge(model="deepseek-gpu:latest") # Probando el alias
    if bridge.is_active:
        print(bridge.ask_coder("Genera una función simple en Verse para imprimir 'Hola Mundo'."))
