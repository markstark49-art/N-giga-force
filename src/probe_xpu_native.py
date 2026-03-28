import torch
import os

def probe_intel_xpu():
    print("⚡ [XPU_PROBE] Iniciando detecci?n de silicio Intel (Nativo)...")
    
    try:
        # En PyTorch 2.5+, XPU es un backend nativo
        if hasattr(torch, 'xpu') and torch.xpu.is_available():
            device_count = torch.xpu.device_count()
            print(f"✅ Hardware Detectado: {device_count} dispositivo(s) XPU.")
            for i in range(device_count):
                device_name = torch.xpu.get_device_name(i)
                print(f"🔹 Dispositivo [{i}]: {device_name}")
                
                # Telemetr?a B?sica de VRAM
                props = torch.xpu.get_device_properties(i)
                mem_total = props.total_memory / (1024**3)
                print(f"📊 VRAM Total: {mem_total:.2f} GB")
                print(f"🌀 Xe Cores / EUs: {props.max_compute_units}")
        else:
            print("⚠️ XPU no detectado por PyTorch.")
            if hasattr(torch, 'xpu'):
                print("🔍 Backend XPU presente pero is_available() es False. Revisa drivers.")
            else:
                print("❌ Este binario de PyTorch no tiene soporte XPU.")
            
    except Exception as e:
        print(f"💥 Error durante el sondeo: {str(e)}")

if __name__ == "__main__":
    probe_intel_xpu()
