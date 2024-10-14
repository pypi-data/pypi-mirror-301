import json
import jsonschema
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from aladeen_metadata_extractor.types.errors import ExtractorError, ExtractorValidationError
from aladeen_metadata_extractor.types.misc import TokenUsage
from aladeen_metadata_extractor.types.client import AiClient


class OpenAIClient(AiClient[OpenAI, ChatCompletion]):
    def __init__(self, api_key, model, temperature, max_tokens, prompt):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = prompt

    def _extract_function_arguments(self, completion, schema):
        tool_call = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
        jsonschema.validate(instance=tool_call, schema=schema)

        return tool_call

    def _extract_token_usage(self, completion):
        return TokenUsage(
            prompt_tokens=completion.usage.prompt_tokens,
            completion_tokens=completion.usage.completion_tokens,
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
            raise ExtractorValidationError[ChatCompletion](e, completion)
        except e:
                raise ExtractorError[ChatCompletion](e, completion)

    def _get_messages(self, content):
        messages = []

        if self.prompt is not None:
            messages.append({"role": "system", "content": self.prompt})

        messages.append({"role": "user", "content": content})
        
        return messages

    def execute(self, content, tool_call):
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
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
            messages=self._get_messages(content=content)
        )

        return self._extract_response(completion=completion, schema=tool_call.parameters)
