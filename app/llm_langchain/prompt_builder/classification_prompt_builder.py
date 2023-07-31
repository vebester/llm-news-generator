from typing import Dict, List, Optional, Tuple, Type, Union, Any
# from pydantic import BaseModel, validate_arguments


class ClassificationPromptBuilder:
    """

    """
    def __init__(self, text: str = "",
                 max_categories: int = 5,
                 categories: List[str] = [],
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:

        # self.system_template = """
        #    You are an experienced editor and article writer.
        #    """

        self.system_template = """
            You are a highly intelligent and accurate multi-label classification system.
            """

        self.set_vars(text=text,
                      max_categories=max_categories,
                      categories=categories,
                      input_language=input_language,
                      output_language=output_language,
                      **kwargs)

    def set_vars(self, text: str = "",
                 max_categories: int = 5,
                 categories: List[str] = [],
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:
        self.text = text
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
