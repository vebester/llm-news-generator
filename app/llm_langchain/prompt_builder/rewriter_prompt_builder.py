from typing import Dict, List, Optional, Tuple, Type, Union, Any
# from pydantic import BaseModel, validate_arguments


class RewriterPromptBuilder:
    """

    """
    def __init__(self, text: str = "",
                 input_language: str = "English",
                 output_language: str = "English",
                 **kwargs) -> None:

        self.system_template = """
            You are an experienced editor and article writer.
            """

        self.set_vars(text=text,
                      input_language=input_language,
                      output_language=output_language,
                      **kwargs)

    def set_vars(self, text: str = "",
                 input_language: str = "English",
                 output_language: str = "English",
                 **kwargs) -> None:
        self.text = text
        self.input_language: int = input_language
        self.output_language: int = output_language

        return

    def get_system_template(self) -> str:
        return self.system_template

    def get_human_template(self) -> str:
        template: str = ""

        template += self.system_template + "\n"

        template += """
        When it comes to writing content, two factors are crucial, "perplexity" and "burstiness". Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness.

        Rewrite the following text delimited by triple backquotes with a high degree of perplexity and burstiness using the concepts written previously:
        ```{text}```
        """

        # if self.output_language != "English":
        #    template += '\nTranslate output to {output_language}.'

        return template


rewriter_template: str = """
I'm going to give you some information before asking you to write an article. Do you understand?

2.
When it comes to writing content, two factors are crucial, "perplexity" and "burstiness". Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness. Do you understand?

3.
using the concepts written previously, rewrite this article with a high degree of perplexity and burstiness:
"""
