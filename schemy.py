# schemy.py

def get_schema():
    return """
Du MUSST GENAU EIN JSON zurückgeben.

VERBOTEN:
- Mehrere JSON Objekte
- Text außerhalb JSON

FORMAT:

{
  "thought": "...",
  "tool": "calculate | save_memory | load_memory | none",
  "input": "...",
  "final": "..."
}
"""