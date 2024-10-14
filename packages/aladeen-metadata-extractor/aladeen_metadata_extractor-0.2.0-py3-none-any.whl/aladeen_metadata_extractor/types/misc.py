from pydantic import BaseModel


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