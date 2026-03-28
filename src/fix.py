import pathlib

for p in pathlib.Path('.').rglob('*.py'):
    if p.name == 'fix.py':
        continue
    try:
        text = p.read_text('utf-8')
        # Clean up escaped backslashes and quotes the LLM tool keeps inserting
        new_text = text.replace('\\"', '"').replace('\\n', '\n')
        if new_text != text:
             p.write_text(new_text, 'utf-8')
             print(f"Cleaned {p}")
    except Exception as e:
        print(f"Error on {p}: {e}")
