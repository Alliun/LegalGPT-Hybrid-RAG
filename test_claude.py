from llm.claude_client import ask_claude

response = ask_claude(

    "You are a helpful assistant.",

    "Say hello in one sentence."

)

print(response)