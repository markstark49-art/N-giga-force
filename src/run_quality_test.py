"""
Script de arranque para test_code_quality.py.
Ejecuta con: python run_quality_test.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.swarm.code_inspector import CodeInspector
from agents.swarm.fitness_evaluator import FitnessEvaluator
from agents.swarm.code_quality_gate import CodeQualityGate

GOOD_CODE = '''
def suma(a: int, b: int) -> int:
    """Suma dos enteros."""
    return a + b

class Calculadora:
    """Calculadora simple."""
    def __init__(self):
        self.historial = []

    def sumar(self, a: int, b: int) -> int:
        result = a + b
        self.historial.append(result)
        return result

    def restar(self, a: int, b: int) -> int:
        result = a - b
        self.historial.append(result)
        return result
'''

BAD_CODE = '''
class GodClass:
    def a(self): pass
    def b(self): pass
    def c(self): pass
    def d(self): pass
    def e(self): pass
    def f(self): pass
    def g(self): pass
    def h(self): pass
    def i(self): pass
    def j(self): pass
    def k(self): pass
    def l(self): pass
    def m(self):
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            print("muy anidado")
'''

def run_tests():
    print("\n=== FASE 131: TEST DE CALIDAD DE CODIGO ===\n")
    inspector = CodeInspector()
    evaluator = FitnessEvaluator()
    gate = CodeQualityGate()

    # Test 1: Codigo bueno
    print("TEST 1: Codigo limpio")
    good_report = inspector.analyze_code(GOOD_CODE)
    print(f"  Score: {good_report['score']} | CC avg: {good_report['complexity']['average']}")
    assert good_report["score"] >= 0.7, f"Esperado >= 0.7, obtenido {good_report['score']}"
    print("  PASS\n")

    # Test 2: Codigo malo (God-Class)
    print("TEST 2: Codigo con God-Class")
    bad_report = inspector.analyze_code(BAD_CODE)
    print(f"  Score: {bad_report['score']} | Violaciones: {bad_report['solid']['violations']}")
    assert bad_report["score"] < 0.7, f"Esperado < 0.7, obtenido {bad_report['score']}"
    print("  PASS\n")

    # Test 3: FitnessEvaluator
    print("TEST 3: FitnessEvaluator - mutacion buena vs original malo")
    fitness, full = evaluator.evaluate(GOOD_CODE, original_code=BAD_CODE, sandbox_success=True)
    print(f"  Fitness: {fitness} | Veredicto: {full['verdict']}")
    print(f"  Desglose: {full['breakdown']}")
    assert full["verdict"] == "APROBADO", "Se esperaba APROBADO"
    print("  PASS\n")

    # Test 4: CodeQualityGate rechazo
    print("TEST 4: CodeQualityGate - debe rechazar God-Class")
    gate_result = gate.gate(BAD_CODE, sandbox_ok=True)
    print(f"  Fitness: {gate_result['fitness']} | Veredicto: {gate_result['verdict']}")
    assert gate_result["verdict"] == "RECHAZADO", "Se esperaba RECHAZADO"
    print("  PASS\n")

    print("=== TODOS LOS TESTS PASARON (Fase 131 operativa) ===")

run_tests()
