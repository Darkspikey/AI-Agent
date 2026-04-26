# schemy.py

def get_schema():
    return """
Du MUSST IMMER valides JSON zurückgeben.

FORMAT:

{
  "thought": "was du denkst",
  "tool": "calculate | save_memory | load_memory | none",
  "input": "string",
  "final": "string oder leer"
}

REGELN:
- KEIN Text außerhalb JSON
- IMMER JSON
"""