# agent.py
import ollama
import json

from tools import calculate, save_memory, load_memory, is_valid_calculation
from schemy import get_schema


SYSTEM_PROMPT = """
Du bist ein Multi-Step AI Agent.

TOOLS:
- calculate(expression)
- save_memory(text)
- load_memory()

ARBEITSWEISE:
1. Denke (thought)
2. Wähle Tool
3. Führe aus
4. Wiederhole bis fertig

Wenn fertig:
→ tool = "none"
→ final setzen
"""


TOOLS = {
    "calculate": calculate,
    "save_memory": save_memory,
    "load_memory": load_memory
}


def run_agent(user_input):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": get_schema()},
        {"role": "user", "content": user_input}
    ]

    max_steps = 5

    for step in range(max_steps):

        response = ollama.chat(
            model="mistral",
            messages=messages,
            options={"temperature": 0}
        )

        output = response["message"]["content"]
        print(f"\nSTEP {step+1} RAW:", output)

        # 🔥 JSON PARSE
        try:
            data = json.loads(output)
        except:
            return "❌ JSON Fehler"

        thought = data.get("thought")
        tool = data.get("tool")
        arg = data.get("input", "")
        final = data.get("final", "")

        print("🧠 Thought:", thought)

        # ✅ FINAL
        if tool == "none":
            return final

        # 🔧 TOOL EXECUTION
        if tool == "calculate":
            if not is_valid_calculation(arg):
                return "❌ invalid calculation"

            result = calculate(arg)

        elif tool in TOOLS:
            result = TOOLS[tool](arg)

        else:
            return "❌ unknown tool"

        print("🔧 Tool Result:", result)

        # 🔁 Ergebnis zurück ins Modell
        messages.append({
            "role": "assistant",
            "content": json.dumps({
                "result": result
            })
        })

    return "❌ Max Steps erreicht"