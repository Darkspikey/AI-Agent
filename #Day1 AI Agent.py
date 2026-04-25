#Day1 AI Agent
import ollama
import json

conversation = []

def chat(user_input):
    conversation.append({"role": "user", "content": user_input})
    response = ollama.chat( model="llama3",
                            messages=conversation)        
    messages = response["message"]

    if "tools_calls" in messages:
        for tool_call in messages["tool_calls"]:
            if tool_call["name"] == "calculator":
                expression = tool_call["arguments"]["expression"]
    reply = response["message"]["content"]
    conversation.append({"role": "assistant", "content": reply})    
    return reply


while True:
    user_input = input("Du: ")
    
    if user_input.lower() in ["exit", "quit"]:
        break
    
    answer = chat(user_input)
    print("Agent:", answer)
