import os
from dotenv import load_dotenv

load_dotenv()
endpoint = os.environ.get("AZURE_AI_CHAT_ENDPOINT")
key = os.environ.get("AZURE_AI_CHAT_KEY")

def sample_chat_completions_with_history():
    
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
    from azure.core.credentials import AzureKeyCredential

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    messages = [
        SystemMessage(
            content="You are an helpful English teacher that teaches English to students. Your replies are short, no more than two sentences."
        ),
        UserMessage(content="What year was construction of the international space station mostly done?"),
    ]

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)

    messages.append(AssistantMessage(content=response.choices[0].message.content))
    messages.append(UserMessage(content="And what was the estimated cost to build it?"))

    response = client.complete(messages=messages)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    sample_chat_completions_with_history()