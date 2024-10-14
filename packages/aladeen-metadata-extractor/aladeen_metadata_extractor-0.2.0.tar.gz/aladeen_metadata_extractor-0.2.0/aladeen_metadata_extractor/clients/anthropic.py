import jsonschema
from anthropic import Anthropic
from anthropic.types.message import Message

from aladeen_metadata_extractor.types.errors import ExtractorError, ExtractorValidationError
from aladeen_metadata_extractor.types.misc import TokenUsage
from aladeen_metadata_extractor.types.client import AiClient


class AnthropicClient(AiClient[Anthropic, Message]):
    def __init__(self, api_key, model, temperature, max_tokens, prompt):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = prompt

    def _extract_function_arguments(self, completion, schema):
        tool_call = completion.content[0].input
        jsonschema.validate(instance=tool_call, schema=schema)

        return tool_call

    def _extract_token_usage(self, completion):
        return TokenUsage(
            prompt_tokens=completion.usage.input_tokens,
            completion_tokens=completion.usage.output_tokens,
        )
    
    def _serialize_completion(self, completion):
        return completion.to_json(indent=0)

    def _extract_response(self, completion, schema):
        try:
            return (
                self._extract_function_arguments(completion=completion, schema=schema),
                self._extract_token_usage(completion=completion),
                self._serialize_completion(completion=completion)
            )
        except jsonschema.exceptions.ValidationError as e:
            raise ExtractorValidationError[Message](e, completion)
        except e:
                raise ExtractorError[Message](e, completion)

    def _get_messages(self, content):
        return [
            {"role": "user", "content": content}
        ]

    def execute(self, content, tool_call):
        completion = self.client.messages.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            tools=[
                {
                    "name": tool_call.name,
                    "description": tool_call.description,
                    "input_schema": tool_call.parameters,
                }
            ],
            tool_choice={"type": "tool", "name": tool_call.name},
            system=self.prompt,
            messages=self._get_messages(content=content)
        )

        return self._extract_response(completion=completion, schema=tool_call.parameters)
