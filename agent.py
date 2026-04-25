import ollama
import json
from tools import safe_calculate

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Mathematische Berechnung",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]

available_functions = {
    "calculate": safe_calculate
}

conversation = [
    {
        "role": "system",
        "content": "Du bist ein AI-Agent. Nutze Tools wenn nötig."
    }
]

def run_agent(user_input):
    conversation.append({"role": "user", "content": user_input})

    for _ in range(5):
        response = ollama.chat(
            model="mistral",
            messages=conversation,
            tools=tools
        )

        message = response["message"]

        if "tool_calls" in message:
            for tool_call in message["tool_calls"]:
                name = tool_call["function"]["name"]
                args = json.loads(tool_call["function"]["arguments"])

                result = available_functions[name](**args)

                conversation.append({
                    "role": "tool",
                    "content": result
                })
        else:
            reply = message["content"]
            conversation.append({"role": "assistant", "content": reply})
            return reply

    return "Max steps erreicht"