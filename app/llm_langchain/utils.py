import requests
import json
from bs4 import BeautifulSoup
from markdownify import markdownify as md

import os

# os.environ["YA_IAM_TOKEN"] = ""
# os.environ["YA_FOLDER_ID"] = ""


import openai


def get_initial_message():
    messages = [
        {"role": "system", "content": "You are a helpful AI Tutor. Who answers brief questions about AI."},
        {"role": "user", "content": "I want to learn AI"},
        {"role": "assistant", "content": "That's awesome, what do you want to know about AI"}
    ]
    return messages


def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response['choices'][0]['message']['content']


def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


def pull_from_website(url: str) -> str:

    # Doing a try in case it doesn't work
    try:
        response = requests.get(url)
    except:
        # In case it doesn't work
        print("Whoops, error")
        return

    # Put your response in a beautiful soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get your text
    text = soup.get_text()

    # Convert your html to markdown. This reduces tokens and noise
    text = md(text)

    return text


def yandex_translate(target_language, texts_list):

    body = {
        "targetLanguageCode": target_language,
        "texts": texts_list,
        "folderId": os.environ.get("YA_FOLDER_ID")
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(os.environ.get('YA_IAM_TOKEN'))
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers)

    response_text = json.loads(response.text)

    return (response_text)
