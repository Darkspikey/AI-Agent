from agent import run_agent

while True:
    user_input = input("Du: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    answer = run_agent(user_input)
    print("Agent:", answer)