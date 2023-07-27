from enum import Enum

from typing import Dict, List, Mapping, Optional, Sequence, Tuple, Type, Union, Any
from pydantic import BaseModel, validate_arguments

# import os
from langchain.llms import OpenAI
from langchain import LLMChain
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.embeddings import OpenAIEmbeddings

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

ROLE_CLASS_MAP = {
    "assistant": AIMessage,
    "user": HumanMessage,
    "system": SystemMessage
}


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    conversation: List[Message]



from .utils import *


class LLMLangChain:
    """

    """
    def __init__(self, config: Dict[str, Any],
                 **kwargs) -> None:
        self.config: Dict[str, Any] = config
        self.model_name: str = config["model_name"]
        self.openai_api_key: str = config["OPENAI_API_KEY"]

        if self.openai_api_key is None or self.openai_api_key == "":
            print("OPENAI_API_KEY is not set")
            # exit(1)
        # else:
        #    print(
        #        f"OPENAI_API_KEY is set: {self.openai_api_key[0:3]}...{self.openai_api_key[-4:]}")

        self.llm = None

        return

    def open_ai(self, **kwargs) -> Optional[OpenAI]: # OpenAI | None:
        if self.openai_api_key is None or self.openai_api_key == "":
            print("OPENAI_API_KEY is not set")
            return None
        # print(
        #    f"ChatOpenAI OPENAI_API_KEY is set: {self.openai_api_key[0:3]}...{self.openai_api_key[-4:]}")

        self.llm = OpenAI(
            model=self.model_name,
            openai_api_key=self.openai_api_key,
            **kwargs)
        return self.llm

    def chain(self, prompt: str) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=prompt)

    # staticmethod
    def system_message(self, content: str = "You are a helpful assistant.") -> Any:
        # return content
        return SystemMessage(content=content)

    # staticmethod
    def human_message(self, content: str) -> Any:
        # return content
        return HumanMessage(content=content)

    # staticmethod
    def ai_message(self, content: str) -> Any:
        # return content
        return AIMessage(content=content)

    def make_prompt_from_template(template: str,
                                  input_variables: list = [],
                                  translate: bool = False) -> str:

        prompt = PromptTemplate(
            input_variables=input_variables,
            template=template)
        if translate:
            pass
            # translated_text = yandex_translate('en',
            #    [text])['translations'][0]['text']
            # text = prompt.format(text=translated_text)
            # text = prompt
        return prompt


# def make_openai_response(prompt):
#    llm = OpenAI(temperature=0.5, max_tokens=1024)
#    open_ai_response = llm(prompt)
#    return (open_ai_response)


# open_ai_response = make_openai_response(translate_and_make_prompt(phrase))
# ya_translate_response = yandex_translate('ru', [open_ai_response])
# print(ya_translate_response['translations'][0]['text'])
