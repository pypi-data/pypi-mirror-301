from pydantic import BaseModel
from typing import List, Dict, Union


class QuestionAnsweringSystemPrompt(BaseModel):
    system_prompt: str = (
        """Answer the user's question based on the given information. Do NOT make up any facts."""
    )
    context_documents: List[str] = []
    user_query: str = ""

    @property
    def compiled_system_prompt(self):
        return self.system_prompt + "\n\n".join(self.context_documents)

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.compiled_system_prompt},
            {"role": "user", "content": self.user_query},
        ]

    def compile(self):
        return self.compiled_system_prompt


class SummarisationSystemPrompt(BaseModel):
    text_to_summarise: str
    n_sentences: int

    @property
    def system_prompt(self) -> str:
        return f"""Summarise the user's text into the smallest number of points possible. It must NOT be more than {str(self.n_sentences)} sentences.
Ignore the following from the text:
- If the text contains comments posted by people, ignore such comments.
- If it contains alerts about accepting cookies, information on cookies, etc. ignore such alerts.

Make sure to include the following in your summary:
- Ensure that your summary contains the technical points and language used in the original text.
- Include all the technical points discussed in the user's text.
"""

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.text_to_summarise},
        ]

    def compile(self):
        return self.system_prompt


class QueryRoutingSystemPrompt(BaseModel):
    system_prompt: str = (
        """Return the most suitable option that this request is related to.
Only return the name of the option, and nothing else, or your response will not be parsed correctly!"""
    )
    routes: List[str] = []
    query: str = ""

    @property
    def compiled_system_prompt(self):
        return f"{self.system_prompt}\n- " + "\n- ".join(self.routes)

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.compiled_system_prompt},
            {"role": "user", "content": self.query},
        ]

    def compile(self):
        return self.compiled_system_prompt


class TableDescriptionGenerationSystemPrompt(BaseModel):
    table_to_describe: str
    n_sentences: int

    @property
    def system_prompt(self) -> str:
        return f"""Describe this table in the smallest number of points possible. It must NOT be more than {str(self.n_sentences)} sentences.
In your description, mention the various columns and the type of data populated across rows.
Ensure that your summary contains the technical points and language used in the original text.
"""

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.table_to_describe},
        ]

    def compile(self):
        return self.system_prompt


class TableReformattingSystemPrompt(BaseModel):
    table_to_reformat: str

    @property
    def system_prompt(self) -> str:
        return f"""You are given a table in Markdown format.
There might have been some errors while parsing this table from a document.
Rewrite the table so that these errors are resolved.
- Carefully compare the column headers to the data in the respective columns. Ensure that they are meaningfully aligned.
Eg, if the column data contains years, but there is no column header for year, you can add this column header.

- Ensure that there are no empty columns or rows in your response.
- Ensure that none of the data in the given table is changed.

Your response must contain only the corrected table in Markdown text.
Ensure that your response does not contain anything else, or your response will not be parsed correctly!
"""

    @property
    def messages(self):
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.table_to_reformat},
        ]

    def compile(self):
        return self.system_prompt
