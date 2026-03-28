"""TRITON XPU INFERENCE: GEMM/MatMul Benchmark for Intel ARC A750 [FINAL_STABLE]"""
import torch
import triton
import triton.language as tl
import os
import time

# --- CONFIGURACIÓN DE ENTORNO HÍBRIDO (MSVC + oneAPI 2025.3) ---
def setup_xpu_env():
    import subprocess
    # 1. Localizar Visual Studio 2022
    vs_root = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools"
    if not os.path.exists(vs_root):
        vs_root = r"C:\Program Files\Microsoft Visual Studio\2022\Community"
    
    # 2. Capturar vcvarsall para variables de compilación base
    vcvars = os.path.join(vs_root, "VC", "Auxiliary", "Build", "vcvarsall.bat")
    if os.path.exists(vcvars):
        print(f"🔧 [XPU_FORGE] Sincronizando entorno MSVC...")
        cmd = f'"{vcvars}" x64 && set'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

    # 3. Configurar oneAPI 2025.3
    oneapi_root = r"C:\Program Files (x86)\Intel\oneAPI"
    ver = "2025.3"
    icpx = os.path.join(oneapi_root, "compiler", ver, "bin", "icpx.exe")
    lib_path = os.path.join(oneapi_root, "compiler", ver, "lib")
    
    if os.path.exists(icpx):
        os.environ["CC"] = icpx
        os.environ["CXX"] = icpx
        print(f"🚀 [XPU_FORGE] Motor de Forja Intel: {icpx}")

    # Inyectar PATH y LIB
    paths = [
        os.path.join(oneapi_root, "compiler", ver, "bin"),
        lib_path,
        os.path.join(oneapi_root, "mkl", "latest", "windows", "bin")
    ]
    for p in paths:
        if os.path.exists(p):
            os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]
            os.environ["LIB"] = p + os.pathsep + os.environ.get("LIB", "")

    # 4. Flags de Compilación y Linkeo Definitivos
    os.environ["TRITON_XPU_BACKEND"] = "1"
    os.environ["TRITON_XPU_STABLE"] = "1"
    os.environ["SYCL_DISABLE_FSYCL_SYCLHPP_WARNING"] = "1"
    
    # Flags para icpx/Triton
    flags = "/MD -fsycl -DSYCL_DISABLE_FSYCL_SYCLHPP_WARNING"
    os.environ["TRITON_EXTRA_CFLAGS"] = flags
    os.environ["TRITON_EXTRA_LDFLAGS"] = f'{flags} /LIBPATH:"{lib_path}" sycl8.lib'
    os.environ["TRITON_C_FLAGS"] = flags
    os.environ["TRITON_LD_FLAGS"] = os.environ["TRITON_EXTRA_LDFLAGS"]
    
    print("✅ [XPU_FORGE] Entorno Híbrido Sincronizado.")

# --- KERNEL MATMUL (GEMM) ---
@triton.jit
def matmul_kernel(
    a_ptr, b_ptr, c_ptr,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_SIZE_M: tl.constexpr, BLOCK_SIZE_N: tl.constexpr, BLOCK_SIZE_K: tl.constexpr,
    GROUP_SIZE_M: tl.constexpr,
):
    pid = tl.program_id(0)
    num_pid_m = tl.cdiv(M, BLOCK_SIZE_M)
    num_pid_n = tl.cdiv(N, BLOCK_SIZE_N)
    num_pid_in_group = GROUP_SIZE_M * num_pid_n
    group_id = pid // num_pid_in_group
    first_pid_m = group_id * GROUP_SIZE_M
    group_size_m = min(num_pid_m - first_pid_m, GROUP_SIZE_M)
    pid_m = first_pid_m + (pid % group_size_m)
    pid_n = (pid % num_pid_in_group) // group_size_m

    offs_am = (pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)) % M
    offs_bn = (pid_n * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)) % N
    offs_k = tl.arange(0, BLOCK_SIZE_K)
    a_ptrs = a_ptr + (offs_am[:, None] * stride_am + offs_k[None, :] * stride_ak)
    b_ptrs = b_ptr + (offs_k[:, None] * stride_bk + offs_bn[None, :] * stride_bn)

    accumulator = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
    for k in range(0, tl.cdiv(K, BLOCK_SIZE_K)):
        a = tl.load(a_ptrs, mask=offs_k[None, :] < K - k * BLOCK_SIZE_K, other=0.0)
        b = tl.load(b_ptrs, mask=offs_k[:, None] < K - k * BLOCK_SIZE_K, other=0.0)
        accumulator += tl.dot(a, b)
        a_ptrs += BLOCK_SIZE_K * stride_ak
        b_ptrs += BLOCK_SIZE_K * stride_bk

    c_offs_m = (pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M))
    c_offs_n = (pid_n * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N))
    c_ptrs = c_ptr + stride_cm * c_offs_m[:, None] + stride_cn * c_offs_n[None, :]
    c_mask = (c_offs_m[:, None] < M) & (c_offs_n[None, :] < N)
    tl.store(c_ptrs, accumulator, mask=c_mask)

def run_benchmark(M=4096, N=4096, K=4096):
    print(f"🚀 [XPU_INFERENCE] Benchmarking GEMM ({M}x{N}x{K})")
    a = torch.randn((M, K), device='xpu', dtype=torch.float32)
    b = torch.randn((K, N), device='xpu', dtype=torch.float32)
    c = torch.empty((M, N), device='xpu', dtype=torch.float32)

    grid = lambda META: (triton.cdiv(M, META['BLOCK_SIZE_M']) * triton.cdiv(N, META['BLOCK_SIZE_N']),)
    
    # Ejecución
    start = time.time()
    matmul_kernel[grid](
        a, b, c, M, N, K,
        a.stride(0), a.stride(1),
        b.stride(0), b.stride(1),
        c.stride(0), c.stride(1),
        BLOCK_SIZE_M=128, BLOCK_SIZE_N=128, BLOCK_SIZE_K=32,
        GROUP_SIZE_M=8
    )
    torch.xpu.synchronize()
    end = time.time()
    
    tflops = (2 * M * N * K) / (end - start) / 1e12
    print(f"✅ Inferencia Completa: {tflops:.2f} TFLOPS")
    print(f"📊 Latencia: {(end-start)*1000:.2f} ms")
    print(f"📂 VRAM: {torch.xpu.memory_allocated()/1e6:.1f} MB")

if __name__ == '__main__':
    setup_xpu_env()
    if torch.xpu.is_available():
        run_benchmark()
    else:
        print("🚨 XPU NO DISPONIBLE")
