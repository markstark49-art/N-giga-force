import ast
import inspect

def get_chunks(code):
    tree = ast.parse(code)
    chunks = []
    lines = code.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            # En Python 3.8+ tenemos lineno y end_lineno
            start = node.lineno - 1
            end = node.end_lineno
            chunk_code = "\n".join(lines[start:end])
            chunks.append({
                "name": node.name,
                "type": type(node).__name__,
                "start": start,
                "end": end,
                "code": chunk_code
            })
    return chunks

test_code = """
def hello(name):
    print(f"Hello {name}")

class Calculator:
    def add(self, a, b):
        return a + b
"""

if __name__ == "__main__":
    try:
        chunks = get_chunks(test_code)
        for c in chunks:
            print(f"Found {c['type']} {c['name']} (Lines {c['start']+1}-{c['end']})")
            print("---")
            print(c['code'])
            print("---\n")
    except Exception as e:
        print(f"Error: {e}")
