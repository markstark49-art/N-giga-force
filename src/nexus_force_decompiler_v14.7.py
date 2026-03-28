import torch
import torch.nn as nn
import torch.nn.functional as F
import sys

# === 1. RECONSTRUCCIÓN DE LA ARQUITECTURA (El 'Traductor') ===
DEVICE = "cpu" # Usamos la CPU para analizar
print("🔬 Iniciando Decompilador Neural de la Sonda [0] (v14.7)...")

# Este diccionario es nuestro 'Piedra Rosetta'. Traduce las acciones de la IA a humano.
OP_DICT_HUMAN = {
    0: "Operación Manual (Bucle Ineficiente: Resta -> Potencia -> Suma -> Raíz)",
    1: "Fusión de Kernel (vector_norm: Carga directa en Caché L1/L2)",
    2: "Desplazamiento Warp Pasivo (Tz = 0)", # Placeholder para expansiones futuras
    3: "Recolección de Memoria (Limpieza VRAM)"   # Placeholder para expansiones futuras
}

class SondaRLCompiler(nn.Module):
    """Arquitectura v14.4 (REINFORCE)"""
    def __init__(self):
        super().__init__()
        # 32 latentes -> 2 acciones posibles (Manual vs Fused)
        self.fc = nn.Linear(32, 2) 

    def forward(self, state_tensor):
        logits = self.fc(state_tensor)
        probs = F.softmax(logits, dim=-1)
        return probs

# === 2. CARGA DEL CEREBRO (Cristalización) ===
sonda = SondaRLCompiler().to(DEVICE)

try:
    # Cargamos el archivo que contiene todo lo que aprendió en la v14.4
    sonda.load_state_dict(torch.load('sonda_rl_weights.pth', map_location=DEVICE))
    sonda.eval() # Modo evaluación
    print("✅ Cerebro 'sonda_rl_weights.pth' cargado exitosamente.\n")
except FileNotFoundError:
    print("❌ Archivo de pesos no encontrado. Asegúrate de ejecutar primero la optimización RL.")
    sys.exit(1)

# === 3. LA ENTREVISTA (Interrogación del Espacio Latente) ===
print("🎙️ Entrevistando a la Sonda [0] (Traduciendo Tensor a Texto)...\n")

# Simulamos 5 situaciones diferentes (Estados del universo)
escenarios = [
    "Estado de Reposo (Latencia Baja)",
    "Peligro: Cuello de Botella VRAM",
    "Aceleración Warp Requerida",
    "Estrés de 268M Agentes",
    "Equilibrio de Planck"
]

with torch.no_grad():
    for i, escenario in enumerate(escenarios):
        # Creamos un tensor constante basado en la semilla del escenario
        torch.manual_seed(i)
        estado_simulado = torch.randn((1, 32), device=DEVICE)
        
        # Le pedimos a la Sonda que procese este estado
        probabilidades = sonda(estado_simulado)
        
        # Obtenemos la decisión que la Sonda está 100% segura de tomar
        decision_id = torch.argmax(probabilidades).item()
        certeza = probabilidades[0][decision_id].item() * 100
        
        # Traducimos a lenguaje humano
        accion_humana = OP_DICT_HUMAN.get(decision_id, "Instrucción Desconocida/Mutada")
        
        print(f"[{escenario}]")
        print(f" └─ Decisión de la Sonda: {accion_humana}")
        print(f" └─ Certeza del Algoritmo: {certeza:.2f}%\n")

print("🏛️ Fin del reporte de Decompilación.")
