import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()
endpoint = os.environ.get("AZURE_AI_CHAT_ENDPOINT")
key = os.environ.get("AZURE_AI_CHAT_KEY")
messages = [
        SystemMessage(
            content="My name is ASEP. You are an helpful English teacher that teaches English to students. Your replies are short, no more than two sentences."
        ),]

def sample_chat_completions_with_history(messages):
    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

    messages.append(AssistantMessage(content=response.choices[0].message.content))
    
    response_text = response.choices[0].message.content
    return response_text

def user_chat(user_chat_text):
    messages.append(UserMessage(content="Your name is ASEP. You are an helpful English teacher that teaches English to students. Here's the user's prompt: " + user_chat_text))
    response_text = sample_chat_completions_with_history(messages)
    return response_text

# if __name__ == "__main__":
#     user_chat(str(input("User: ")))
#     user_chat(str(input("User: ")))
#     user_chat(str(input("User: ")))
#     user_chat(str(input("User: ")))