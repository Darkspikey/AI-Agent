# agent.py
import ollama
import json
import re

from tools import calculate, save_memory, load_memory, is_valid_calculation
from schemy import get_schema
from reflector import reflect


SYSTEM_PROMPT = """
Du bist ein Multi-Step AI Agent.

WICHTIG:
- IMMER EIN JSON
- KEIN TEXT

TOOLS:
- calculate
- save_memory
- load_memory

FORMAT:

{
  "thought": "...",
  "tool": "...",
  "input": "...",
  "final": "..."sa
}

Wenn fertig:
→ tool = "none"
"""


TOOLS = {
    "calculate": calculate,
    "save_memory": save_memory,
    "load_memory": load_memory
}


def extract_first_json(text):
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)
    for m in matches:
        try:
            return json.loads(m)
        except:
              # Versuch 2: Häufige LLM-Fehler korrigieren (Backslashes)
            try:
                # Maskiert einfache Backslashes, außer sie sind bereits Teil einer validen Sequenz
                fixed_str = m.replace('\\', '\\\\')
                # Manchmal maskiert dies zu viel (z.B. \" zu \\"), das muss man ggf. feintunen
                return json.loads(fixed_str)
            except:
                return None
    return None
    # Findet alles zwischen der ersten { und der LETZTEN } im String   
      


def normalize_expression(expr: str):
    expr = expr.replace("Math.sqrt", "sqrt")
    expr = expr.replace("^", "**")
    return expr


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

        data = extract_first_json(output)

        if not data:
            print("⚠️ RESET")
            messages = messages[:3]
            continue

        thought = data.get("thought")
        tool = data.get("tool")
        arg = data.get("input", "")
        final = data.get("final", "")

        print("🧠 Thought:", thought)

        # 🔥 FINAL + REFLECTION
        if tool == "none":

            reflection = reflect(user_input, last_result, final)
            print("🔍 Reflection:", reflection)

            if reflection.get("correct"):
                return final
            else:
                print("⚠️ Korrigiere Antwort...")
                return reflection.get("fix", final)

        # 🔧 TOOL
        if tool == "calculate":

            arg = normalize_expression(arg)

            if not is_valid_calculation(arg):
                messages.append({
                    "role": "system",
                    "content": f"FEHLER: {arg} ungültig"
                })
                continue

            result = calculate(arg)

        elif tool == "save_memory":
            result = save_memory(arg)

        elif tool == "load_memory":
            result = load_memory()

        else:
            return "❌ unknown tool"

        print("🔧 Tool Result:", result)

        if result == last_result:
            return result
        last_result = result

        messages.append({
            "role": "user",
            "content": f"TOOL RESULT: {result}"
        })

    return "❌ Max Steps erreicht"