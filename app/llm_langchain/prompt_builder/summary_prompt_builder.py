from typing import Dict, List, Optional, Tuple, Type, Union, Any
# from pydantic import BaseModel, validate_arguments


class SummaryPromptBuilder:
    """

    """
    def __init__(self, text: str = "",
                 max_sentences: int = 5, max_chars: int = 300,
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:

        self.system_template = """
            You are an experienced editor and article writer.
            """

        self.set_vars(text=text,
                      max_sentences=int(max_sentences), max_chars=max_chars,
                      input_language=input_language,
                      output_language=output_language,
                      **kwargs)

    def set_vars(self, text: str = "",
                 max_sentences: int = 5, max_chars: int = 300,
                 input_language: str = "English", output_language: str = "English",
                 **kwargs) -> None:
        self.text = text
        self.max_sentences: int = max_sentences
        self.max_chars: int = max_chars
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

        if self.output_language != "English":
            template += '\nTranslate output to {output_language}.'

        # template += ' in an informal, conversational style.'

        # template += """
        #    ```{text}```
        #    SUMMARY:
        #    """

        return template
