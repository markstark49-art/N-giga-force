import os
import time
import sys

# --- CONFIGURACIÓN DE ENTORNO MSVC/ONEAPI ---
def setup_xpu_env():
    import subprocess
    # 1. Entorno MSVC
    vs_root = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"
    if not os.path.exists(vs_root):
        vs_root = r"C:\Program Files\Microsoft Visual Studio\2022\Community"
    
    latest_msvc = None
    vcvars = os.path.join(vs_root, "VC", "Auxiliary", "Build", "vcvarsall.bat")
    if os.path.exists(vcvars):
        print(f"🔧 [XPU_FORGE] Sincronizando MSVC...")
        # Localizar la versión de MSVC primero para usarla en INCLUDE después
        msvc_dir = os.path.join(vs_root, "VC", "Tools", "MSVC")
        if os.path.exists(msvc_dir):
            latest_msvc = sorted(os.listdir(msvc_dir))[-1]
            
        cmd = f'"{vcvars}" x64 && set'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

    # 2. Entorno oneAPI (Rutas críticas de compilador y librerías)
    oneapi_root = r"C:\Program Files (x86)\Intel\oneAPI"
    # Versión específica 2025.3 detectada en el escaneo
    icpx_path = os.path.join(oneapi_root, "compiler", "2025.3", "bin", "icpx.exe")
    
    if os.path.exists(icpx_path):
        os.environ["CC"] = icpx_path
        os.environ["CXX"] = icpx_path
        print(f"🚀 [XPU_FORGE] Usando compilador Intel 2025.3: {icpx_path}")
    
    paths_to_add = [
        os.path.join(oneapi_root, "compiler", "2025.3", "bin"),
        os.path.join(oneapi_root, "compiler", "2025.3", "lib"),
        os.path.join(oneapi_root, "mkl", "latest", "windows", "bin")
    ]
    # 3. Sincronización de Cabeceras (INCLUDE) para icpx
    # Necesitamos las cabeceras de MSVC para que icpx encuentre corecrt.h
    sdk_root = r"C:\Program Files (x86)\Windows Kits\10\Include"
    if os.path.exists(sdk_root):
        latest_sdk = sorted(os.listdir(sdk_root))[-1]
        paths_to_include = [
            os.path.join(sdk_root, latest_sdk, "ucrt"),
            os.path.join(sdk_root, latest_sdk, "shared"),
            os.path.join(sdk_root, latest_sdk, "um")
        ]
        if latest_msvc:
            paths_to_include.append(os.path.join(vs_root, "VC", "Tools", "MSVC", latest_msvc, "include"))
        
        for p in paths_to_include:
            if os.path.exists(p):
                current_include = os.environ.get("INCLUDE", "")
                os.environ["INCLUDE"] = p + os.pathsep + current_include
    
    print("✅ [XPU_FORGE] Entorno Híbrido MSVC + oneAPI + SDK Inyectado.")

# --- BYPASS DEFINITIVO DEL LINKER (LNK1104) ---
sycl_lib_oneapi = r"C:\Program Files (x86)\Intel\oneAPI\compiler\2025.3\lib"
sycl_lib_python = r"C:\Users\Angel\AppData\Local\Programs\Python\Python312\Library\lib"
sycl_include = r"C:\Program Files (x86)\Intel\oneAPI\compiler\2025.3\include"

os.environ["TRITON_XPU_BACKEND"] = "1"
os.environ["TRITON_XPU_STABLE"] = "1"
os.environ["SYCL_DISABLE_FSYCL_SYCLHPP_WARNING"] = "1"

# Forzamos coherencia de C++ Runtime con /MD y rutas absolutas
os.environ["TRITON_EXTRA_CFLAGS"] = f"/MD -fsycl -DSYCL_DISABLE_FSYCL_SYCLHPP_WARNING -I\"{sycl_include}\""
os.environ["TRITON_EXTRA_LDFLAGS"] = (
    f"/MD -fsycl /link "
    f"/LIBPATH:\"{sycl_lib_oneapi}\" "
    f"/LIBPATH:\"{sycl_lib_python}\" "
    "sycl8.lib"
)

setup_xpu_env()
os.environ["TRITON_XPU_BACKEND"] = "1"
os.environ["SYCL_DISABLE_FSYCL_SYCLHPP_WARNING"] = "1"
os.environ["TRITON_XPU_STABLE"] = "1"
os.environ["TRITON_XPU_DUMP_CSRC"] = "1"

# Banderas de Compilación Críticas para Intel SYCL en Windows
# Forzamos /MD (Dynamic Runtime) y apuntamos a sycl8.lib estable
sycl_lib_path_oneapi = r"C:\Program Files (x86)\Intel\oneAPI\compiler\2025.3\lib"
sycl_lib_path_python = r"C:\Users\Angel\AppData\Local\Programs\Python\Python312\Library\lib"
os.environ["TRITON_EXTRA_CFLAGS"] = f"/MD -fsycl -DSYCL_DISABLE_FSYCL_SYCLHPP_WARNING -I\"{os.path.join(sycl_lib_path_oneapi, '..', 'include')}\""
os.environ["TRITON_EXTRA_LDFLAGS"] = f"/MD -fsycl /link /LIBPATH:\"{sycl_lib_path_oneapi}\" /LIBPATH:\"{sycl_lib_path_python}\" sycl8.lib"

# --- INICIALIZACIÓN DE BACKENDS (POST-ENVIRONMENT) ---
import torch
import triton
import triton.language as tl

@triton.jit
def add_kernel(x_ptr, y_ptr, output_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    output = x + y
    tl.store(output_ptr + offsets, output, mask=mask)

def test_add(size=1024*1024):
    print(f"🔹 [TRITON_XPU] Iniciando forja en Intel ARC... (Size: {size})")
    
    # 1. Preparar Tensores en XPU
    x = torch.randn(size, device='xpu')
    y = torch.randn(size, device='xpu')
    output = torch.empty_like(x)
    
    # 2. Configuración de Lanzamiento
    grid = lambda meta: (triton.cdiv(size, meta['BLOCK_SIZE']),)
    
    # 3. Ejecución del Kernel (Compilación JIT automática)
    try:
        start_time = time.time()
        add_kernel[grid](x, y, output, size, BLOCK_SIZE=1024)
        torch.xpu.synchronize()
        end_time = time.time()
        
        # 4. Verificación
        if torch.allclose(output, x + y):
            print(f"✅ SUCCESS: Kernel Triton compilado y ejecutado en {(end_time-start_time)*1000:.2f}ms")
            print(f"📊 VRAM Utilizada: {torch.xpu.memory_allocated()/1e6:.1f} MB")
        else:
            print("❌ FAILURE: Discrepancia en los resultados del kernel.")
            
    except Exception as e:
        print(f"🔥 ERROR DE FORJA: {str(e)}")
        print("💡 TIP: Asegúrate de que MSVC y oneAPI estén en el PATH.")

if __name__ == '__main__':
    if torch.xpu.is_available():
        test_add()
    else:
        print("🚨 XPU NO DISPONIBLE: Verifica los drivers de tu ARC A750.")
