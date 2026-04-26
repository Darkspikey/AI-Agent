# main.py
from agent import run_agent

while True:
    user_input = input("\nDu: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    answer = run_agent(user_input)
    print("Agent:", answer)