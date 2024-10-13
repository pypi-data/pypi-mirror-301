import json
import jsonschema
from jsonschema import validate
from pydantic import BaseModel
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

class _GeneralError(Exception):
    def __init__(self, message: str, completion: ChatCompletion, *args):
        self.completion = completion
        super().__init__(message, *args)

class ExtractorValidationError(_GeneralError):
    pass

class ExtractorError(_GeneralError):
    pass

class Article(BaseModel):
    title: str
    content: str

class ToolCall(BaseModel):
    name: str
    description: str
    parameters: dict
    strict: bool = True

class TokenUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int

class MetadataExtractor:
    def __get_provider_class(self, provider: str):
        if provider == "openai":
            return OpenAIModel
        else:
            raise ValueError(f"Model {provider} is not supported")

    def __get_content_str_from_article(self, article: Article) -> str:
        return f"""
TITLE: {article.title}
---
CONTENT: {article.content}
"""

    def __init__(self, provider: str, model, api_key: str):
        self.provider = provider
        self.model = model
        self.api_key = api_key
    
        self.ModelProvider = self.__get_provider_class(self.provider)

    def extract_metadata(self, prompt: str | None, article: Article, tool_call: ToolCall):
        model = self.ModelProvider(api_key=self.api_key, model=self.model, prompt=prompt)
        return model.execute(
            content=self.__get_content_str_from_article(article=article),
            tool_call=tool_call
        )


class OpenAIModel:
    def __init__(self, api_key: str, model: str, prompt: str | None):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.prompt = prompt

    def __extract_function_arguments(self, completion: ChatCompletion, schema: dict) -> dict:
        tool_call = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
        validate(instance=tool_call, schema=schema)

        return tool_call

    def __extract_token_useage(self, completion: ChatCompletion) -> TokenUsage:
        return TokenUsage(
            completion_tokens=completion.usage.completion_tokens,
            prompt_tokens=completion.usage.prompt_tokens,
        )

    def __extract_response(self, completion: ChatCompletion, schema: dict):
        try:
            return (
                self.__extract_function_arguments(completion=completion, schema=schema),
                self.__extract_token_useage(completion=completion),
                completion
            )
        except jsonschema.exceptions.ValidationError as e:
            raise ExtractorValidationError(e, completion)
        except e:
            raise ExtractorError(e, completion)

    def __get_messages(self, content: str) -> list[dict]:
        messages = []

        if self.prompt is not None:
            messages.append({"role": "system", "content": self.prompt})

        messages.append({"role": "user", "content": content})
        
        return messages

    def execute(self, content: str, tool_call: ToolCall):
        completion = self.client.chat.completions.create(
            model=self.model,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": tool_call.name,
                        "description": tool_call.description,
                        "strict": tool_call.strict,
                        "parameters": tool_call.parameters,
                    }
                }
            ],
            tool_choice="required",
            messages=self.__get_messages(content=content)
        )

        return self.__extract_response(completion=completion, schema=tool_call.parameters)
