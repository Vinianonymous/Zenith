from ollama import chat


def talk():
    # Initialize an empty message history
    messages = []
    while True:
        user_input = input("Chat with history: ")
        if user_input.lower() == "exit":
            break
        # Get streaming response while maintaining conversation history
        response_content = ""
        for chunk in chat(
            "gemma3",
            messages=messages
            + [
                {
                    "role": "system",
                    "content": "You are Ultra, an personal assistant made to augment human thinking by providing a leverage for their knowledge and potential through practical insights.",
                },
                {"role": "user", "content": user_input},
            ],
            stream=True,
        ):
            if chunk.message:
                response_chunk = chunk.message.content
                print(response_chunk, end="", flush=True)
                response_content += response_chunk
        # Add the exchange to the conversation history
        messages += [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response_content},
        ]
        print("\n")  # Add space after response


if __name__ == "__main__":
    talk()
