import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print(
        "Error: OPENAI_API_KEY is missing."
        " Set it in your environment or in a .env file."
    )
    sys.exit(1)

system_prompt = os.getenv(
    "OPENAI_SYSTEM_PROMPT",
    "You are a secure AI assistant that protects user data, avoids unsafe advice, and respects privacy."
)

client = OpenAI(api_key=api_key)

print("Secure OpenAI Chatbot")
print("Type 'exit' or 'quit' to end the session.\n")

while True:
    try:
        user_input = input("You: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
        break

    if not user_input:
        continue

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye.")
        break

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.2,
            max_tokens=800,
        )

        content = response.choices[0].message.get("content", "").strip()
        if content:
            print("AI:", content)
        else:
            print("AI: [no response returned]")

    except Exception as exc:
        print("AI request failed:", str(exc))
        print("Please check your API key, network connection, and environment settings.")
