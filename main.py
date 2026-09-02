from agent.agent import Agent

agent = Agent()

response = agent.chat("Hello, who are u ?")
print("AI:", response)

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Good bye")
        break

    response = agent.chat(user_input)

    print("AI:", response)