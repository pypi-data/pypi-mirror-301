from typing import Literal, Union
from aladeen_metadata_extractor.clients.openai import OpenAIClient
from aladeen_metadata_extractor.clients.anthropic import AnthropicClient
from aladeen_metadata_extractor.types.misc import Article, ToolCall


class MetadataExtractor:
    def __get_provider_class(self, provider: Union[Literal["openai"], Literal["anthropic"]]):
        if provider == "openai":
            return OpenAIClient
        elif provider == "anthropic":
            return AnthropicClient
        else:
            raise ValueError(f"Model {provider} is not supported")

    def __get_content_str_from_article(self, article: Article) -> str:
        return f"""
TITLE: {article.title}
---
CONTENT: {article.content}
"""

    def __init__(self, provider: str, model, temperature: float, max_tokens: int, api_key: str):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
    
        self.ModelProvider = self.__get_provider_class(self.provider)

    def execute(self, prompt: str | None, article: Article, tool_call: ToolCall):
        model = self.ModelProvider(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            prompt=prompt
        )

        return model.execute(
            content=self.__get_content_str_from_article(article=article),
            tool_call=tool_call
        )
