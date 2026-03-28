import time
def calcular_fibonacci(n):
    # Versión OPTIMIZADA (iterativa)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

if __name__ == "__main__":
    result = calcular_fibonacci(30)
    print(result)
