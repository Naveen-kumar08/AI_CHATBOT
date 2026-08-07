from chatbot import ask_groq

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Hello"
    }
]

print(ask_groq(messages))