import os
import sys

import requests

API_KEY = os.environ.get("API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"


def send_to_chatgpt_api(messages, model="gpt-3.5-turbo"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
        "model": model,
        "messages": messages
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        # Process the response here
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None


def send_and_add_to_conversation(conversation, new_msg):
    conversation.append({"role": "user", "content": new_msg})
    response = send_to_chatgpt_api(conversation)
    if response:
        assistant_response = response['choices'][0]['message']['content']
        # print(f"Assistant: {assistant_response}")
        conversation.append({"role": "assistant", "content": assistant_response})
        return assistant_response


def get_context():
    file_name = sys.argv[1]
    result = []

    with open(file_name, "r") as f:
        while True:
            chunk = f.read(2000)
            if not chunk:
                break
            result.append(chunk)
    return result


def main():
    context = get_context()
    conversation = []
    # send_and_add_to_conversation(conversation,
    #                              "Im going to give you the content of a file in the following prompts. they'll serve as the context for my following questions. Reply only 'OK' until I type '--Context Ends--'")

    # Add a new user message to the conversation
    for context_msg in context:
        conversation.append({"role": "user", "content": context_msg})
        # send_and_add_to_conversation(conversation, context_msg)

    # send_and_add_to_conversation(conversation, "--Context Ends--")

    print("Context loaded")
    while True:
        question = input("Q: ")
        if question == '##':
            question_parts = []
            question = input("> ")
            while question != '###':
                question_parts.append(question)
                question = input("> ")
            question = '\n'.join(question_parts)

        answer = send_and_add_to_conversation(conversation, question)
        # Generate answer here
        if answer:
            answer = f"A: {answer}"
            print(answer)


if __name__ == "__main__":
    main()
