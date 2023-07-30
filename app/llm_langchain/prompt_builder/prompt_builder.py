from typing import Dict, List, Optional, Tuple, Type, Union, Any
# from pydantic import BaseModel, validate_arguments


class PromptBuilder:
    """

    """

    def __init__(self, text: str = "", text_category: str = "",
                 max_sentences: int = 5, max_chars: int = 300,
                 max_categories: int = 5,
                 categories: List[str] = [],
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:

        self.system_template = """
            You are an experienced editor and article writer.
            """
        self.system_classification_template = """
            You are a highly intelligent and accurate multi-label classification system.
            """

        self.set_vars(text=text, text_category=text_category,
                      max_sentences=int(max_sentences), max_chars=max_chars,
                      max_categories=max_categories,
                      categories=categories,
                      input_language=input_language,
                      output_language=output_language,
                      **kwargs)

    def set_vars(self, text: str = "", text_category: str = "",
                 max_sentences: int = 5, max_chars: int = 300,
                 max_categories: int = 5,
                 categories: List[str] = [],
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:
        self.text = text
        self.text_category: str = text_category
        self.max_sentences: int = max_sentences
        self.max_chars: int = max_chars
        self.max_categories = max_categories
        self.categories = categories
        self.input_language: int = input_language
        self.output_language: int = output_language

        return

    def get_system_template(self) -> str:
        return self.system_template

    def get_human_template(self) -> str:
        template: str = ""

        template += self.system_template + "\n"

        template += """
        Write a concise summary of the following text delimited by triple backquotes, which covers the key points of the text.
        ```{text}```
        SUMMARY:
        """
        # Саммари может состоять до {max_sentences} предложений и должен иметь длину не более {max_chars} символов.
        # template += '\nThe summary can consist up to {max_sentences} sentences and must have no more than {max_chars} chars length.'

        # if self.input_language != self.output_language:
        #   template += '\nTranslate output from {input_language} to {output_language}.'

        # if self.output_language != "English":
        #    template += '\nTranslate output to {output_language}.'

        # template += ' in an informal, conversational style.'

        # template += """
        #    ```{text}```
        #    SUMMARY:
        #    """

        return template

    def get_system_classification_template(self) -> str:
        return self.system_classification_template

    def get_human_classification_template(self) -> str:
        template: str = ""

        template += self.system_classification_template + "\n"

        template += """
        Classify the following text delimited by triple backquotes into {max_categories} most appropriate categories from the values in given category list:
        {categories}.
        When analyzing do not use categories that not in given category list.
        Write output into category list up to {max_categories} most relevant categories.
        Do not include in output list categories that not in given category list and categories with zero rank.
        ```{text}```
        OUTPUT:
        """
        #  in JSON format

        # Записать выходные данные в список категорий
        #template += """
        #Classify the following text delimited by triple backquotes as one of the following appropriate Categories:
        #{categories}
        #```{text}```
        #CATEGORIES:
        #"""

        return template


rewriter_template: str = """""
I'm going to give you some information before asking you to write an article. Do you understand?

2.
When it comes to writing content, two factors are crucial, "perplexity" and "burstiness." Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness. Do you understand?

3.
using the concepts written previously, rewrite this article with a high degree of perplexity and burstiness:
"""
