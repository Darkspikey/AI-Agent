# agent.py
import ollama
import json
import re

from tools import calculate, save_memory, load_memory, is_valid_calculation
from schemy import get_schema

SYSTEM_PROMPT = """
Du bist ein Multi-Step AI Agent.

WICHTIG:
- IMMER JSON
- NIEMALS normalen Text
- NIEMALS erklären

TOOLS:
- calculate(expression) → NUR Python Syntax!

REGELN FÜR calculate:
- Verwende NUR:
  sqrt(x)
  + - * /
- NIEMALS:
  Math.sqrt
  pow()
  ^
  oder andere Sprachen

Beispiel:
Richtig: sqrt(64)
Falsch: Math.sqrt(64)

FORMAT:

{
  "thought": "...",
  "tool": "calculate | save_memory | load_memory | none",
  "input": "...",
  "final": "..."
}
STOP REGEL:

Wenn du das Ergebnis bereits kennst:
→ KEIN Tool mehr verwenden
→ tool = "none"
→ final setzen

VERBOTEN:
- calculate erneut auf gleiche Eingabe

Wenn fertig:
→ tool = "none"
"""


TOOLS = {
    "calculate": calculate,
    "save_memory": save_memory,
    "load_memory": load_memory
}

def normalize_expression(expr: str):
    expr = expr.replace("Math.sqrt", "sqrt")
    expr = expr.replace("^", "**")
    return expr

def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return None
        return None


def run_agent(user_input):
    last_result = None

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": get_schema()},
        {"role": "user", "content": user_input}
    ]

    max_steps = 6

    for step in range(max_steps):

        response = ollama.chat(
            model="mistral",
            messages=messages,
            options={"temperature": 0}
        )

        output = response["message"]["content"]
        print(f"\nSTEP {step+1} RAW:", output)

        data = safe_json_parse(output)

        if not data:
            print("⚠️ Kein JSON → Retry")
            messages.append({
                "role": "system",
                "content": "FEHLER: Nur JSON antworten!"
            })
            continue

        thought = data.get("thought")
        tool = data.get("tool")
        arg = data.get("input", "")
        final = data.get("final", "")

        print("🧠 Thought:", thought)
      
        if tool == "none":
            return final

        if tool == "calculate":

            arg = normalize_expression(arg)

            if not is_valid_calculation(arg):
                messages.append({
                    "role": "system",
                    "content": f"FEHLER: '{arg}' ist ungültig. Nutze nur sqrt(x) und + - * /"
                })
                continue

            result = calculate(arg)

        elif tool in TOOLS:
            result = TOOLS[tool](arg)

        else:
            return "❌ unknown tool"

        print("🔧 Tool Result:", result)

        # 🔥 LOOP BREAK
        if result == last_result:
            return result
        last_result = result
        # 🔥 WICHTIGSTER FIX
        messages.append({
            "role": "user",
            "content": f"TOOL RESULT: {result}. Wenn korrekt, beende mit tool='none'."
        })

    return "❌ Max Steps erreicht"