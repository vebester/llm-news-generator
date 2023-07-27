from typing import Dict, List, Mapping, Optional, Tuple, Type, Union, Any
from pydantic import BaseModel, validate_arguments


class PromptBuilder:
    """

    """

    def __init__(self, text: str = "", text_category: str = "",
                 n_negative: int = 0, n_positive: int = 0,
                 max_sentences: int = 5, max_chars: int = 300,
                 max_arguments: int = 3,
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:
        self.set_vars(text=text, text_category=text_category,
                      n_negative=n_negative, n_positive=n_positive,
                      max_sentences=int(max_sentences), max_chars=max_chars,
                      max_arguments=int(max_arguments),
                      output_language=output_language,
                      **kwargs)

    def set_vars(self, text: str = "", text_category: str = "",
                 n_negative: int = 0, n_positive: int = 0,
                 max_sentences: int = 5, max_chars: int = 300,
                 max_arguments: int = 3,
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:
        self.text = text
        self.text_category: str = text_category
        self.n_negative: int = n_negative
        self.n_positive: int = n_positive
        self.n_comments: int = n_negative + n_positive

        self.max_sentences: int = max_sentences
        self.max_chars: int = max_chars
        self.max_arguments: int = max_arguments

        self.input_language: int = input_language
        self.output_language: int = output_language
        return

    def get_human_template(self) -> str:
        human_template: str = ""
        if self.text != "":
            human_template = 'Based on the topic text delimited by triple backticks ```{text}```'
            if self.text_category != "":
                human_template += ' taking in account topic category "{text_category}"'
        else:
            human_template = 'Based on the topic category delimited by triple backticks ```{text_category}```'
        human_template += ' generate'
        if self.n_negative:
            human_template += ' {n_negative} negative'
            if self.n_positive:
                human_template += ' and {n_positive} positive'
        elif self.n_positive:
            human_template += ' {n_positive} positive'
        human_template += ' comment'
        if self.n_comments > 1:
            human_template += 's'

        human_template += ' in an informal, conversational style.'

        # Каждый сгенерированный комментарий может состоять от 1 до {max_sentences} предложений и должен иметь длину не более {max_chars} символов.
        human_template += '\nEach comment can consist randomly from 1 to {max_sentences} sentences and must have no more than {max_chars} chars length.'

        
        if self.n_negative and self.max_arguments:
            # Каждый отрицательный комментарий может содержать случайным образом от 1 до {max_arguments} аргументов против содержания темы.
            human_template += '\nEach negative comment can contain randomly from 1 to {max_arguments} arguments against topic content.'
        if self.n_positive and self.max_arguments:
            # Каждый положительный комментарий может содержать случайным образом от 1 до {max_arguments} аргументов для содержания темы.
            human_template += '\nEach positive comment can contain randomly from 1 to {max_arguments} arguments for topic content.'

        
        if self.n_negative:
            # Каждый отрицательный комментарий может содержать случайным образом от 1 до {max_arguments} аргументов против содержания темы.
            human_template += '\nEach negative comment mark with label "negative".'
        if self.n_positive:
            # Каждый положительный комментарий может содержать случайным образом от 1 до {max_arguments} аргументов для содержания темы.
            human_template += '\nEach positive comment mark with label "positive".'

        # human_template += '\nEach generated comment mark with label "negative" or "positive".'

        # if self.input_language != self.output_language:
            #human_template += '\nTranslate output from {input_language} to {output_language}.'
            
        if self.output_language != "English":
            human_template += '\nTranslate output to {output_language}.'

        # Отформатируйте выходные данные в формате JSON в виде списка сгенерированных объектов комментариев со следующими ключами
        human_template += """
        Format the output as JSON with list of generated comment objects with the following keys:
        label 
        comment        
        """
        # % YOUR RESPONSE:

        return human_template
