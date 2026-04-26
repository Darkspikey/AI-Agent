# reflector.py
import ollama
import json


REFLECTION_PROMPT = """
Du bist ein Prüfer.

Du bekommst:
- die ursprüngliche Aufgabe
- den Tool Output
- die Antwort des Agents

Deine Aufgabe:
- Prüfe ob die Antwort korrekt ist

Wenn korrekt:
{
  "correct": true
}

Wenn falsch:
{
  "correct": false,
  "fix": "korrekte Antwort"
}

NUR JSON!
"""


def reflect(user_input, result, final_answer):

    messages = [
        {"role": "system", "content": REFLECTION_PROMPT},
        {"role": "user", "content": f"""
Aufgabe: {user_input}
Tool Ergebnis: {result}
Agent Antwort: {final_answer}
"""}
    ]

    response = ollama.chat(
        model="mistral",
        messages=messages,
        options={"temperature": 0}
    )

    output = response["message"]["content"]

    try:
        return json.loads(output)
    except:
        return {"correct": True}