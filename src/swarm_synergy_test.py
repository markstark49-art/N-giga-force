from ollama_bridge import OllamaBridge
import os

class SwarmOrchestrator:
    """
    N-GIGA-FORGE v10.5 (SWARM EDITION)
    Combina Geometría (N-Giga) con Lógica IA (DeepSeek Coder).
    """
    def __init__(self):
        self.bridge = OllamaBridge(model="deepseek-gpu:latest")
        print("🚀 N-GIGA-FORGE: Vínculo Neuronal Local Activado.")

    def run_synergy_test(self):
        # 1. Petición de Lógica Avanzada a DeepSeek Coder
        prompt = (
            "Escribe una función de Verse llamada 'DisappearSequence' "
            "que reciba un creative_prop y lo oculte (Hide()) durante 2 segundos, "
            "luego lo vuelva a mostrar (Show()). Debe ser una función suspends."
        )
        
        print("\n🧠 Solicitando lógica procedural a DeepSeek...")
        logic_code = self.bridge.ask_coder(prompt)
        
        # 2. Construcción del Template Verse final
        verse_template = f"""
using {{ /Fortnite.com/Devices }}
using {{ /Verse.org/Simulation }}
using {{ /EpicGames.com/Temporary/SpatialMath }}
using {{ /Verse.org/Assets }}

# ♾️ N-GIGA-FORGE x DEEPSEEK CODER: SYNERGY TEST V1
# Lógica generada dinámicamente por la IA local.

synergy_deathrun_test := class(creative_device):

    @editable PlatformAsset : creative_prop_asset = DefaultCreativePropAsset

    # --- Lógica Generada por DeepSeek ---
    {logic_code}

    OnBegin<override>()<suspends>:void=
        Print("🌪️ Iniciando Prueba de Sincronía Swarm (N-Giga x DeepSeek)...")
        # Instanciamos una plataforma de prueba
        Transform := transform{{Translation := vector3{{X:=0.0, Y:=0.0, Z:=500.0}}, Rotation := IdentityRotation()}}
        SpawnResult := SpawnProp(PlatformAsset, Transform)
        
        if (Prop := SpawnResult(0)?):
            Print("✨ Plataforma materializada. Iniciando secuencia IA...")
            loop:
                DisappearSequence(Prop)
                Sleep(3.0)
"""
        
        with open("synergy_test.verse", "w", encoding="utf-8") as f:
            f.write(verse_template)
            
        print("\n✅ PRUEBA DE SINERGIA COMPLETADA: 'synergy_test.verse' generado.")

if __name__ == "__main__":
    orchestrator = SwarmOrchestrator()
    orchestrator.run_synergy_test()
