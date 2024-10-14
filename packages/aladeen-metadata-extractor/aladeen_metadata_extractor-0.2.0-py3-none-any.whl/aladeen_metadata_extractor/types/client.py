from abc import ABC, abstractmethod
from typing import Generic, Optional, List, Dict, Tuple, TypeVar

from aladeen_metadata_extractor.types.misc import TokenUsage, ToolCall

TClient = TypeVar('TClient')
TChatCompletion = TypeVar('TChatCompletion')


class AiClient(ABC, Generic[TClient, TChatCompletion]):
    client: TClient
    model: str
    temperature: float
    max_tokens: int
    prompt: Optional[str]

    @abstractmethod
    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int, prompt: Optional[str] = None) -> None:
        """
        Initializes the client with the given parameters.

        Args:
            api_key (str): The API key for the client.
            model (str): The model name to use.
            temperature (float): The temperature for the model.
            max_tokens (int): The maximum number of tokens to generate.
            prompt (Optional[str]): The system prompt, if any.
        """
        pass

    @abstractmethod
    def _extract_function_arguments(self, completion: TChatCompletion, schema: dict) -> dict:
        """
        Extracts function arguments from the completion.

        Args:
            completion (TChatCompletion): The completion object from the client.
            schema (dict): The JSON schema to validate against.

        Returns:
            dict: The extracted function arguments.

        Raises:
            ExtractorValidationError: If validation fails.
            ExtractorError: For other extraction errors.
        """
        pass

    @abstractmethod
    def _extract_token_usage(self, completion: TChatCompletion) -> TokenUsage:
        """
        Extracts token usage from the completion.

        Args:
            completion (TChatCompletion): The completion object from the client.

        Returns:
            TokenUsage: The token usage data.
        """
        pass

    @abstractmethod
    def _serialize_completion(self, completion: TChatCompletion) -> str:
        """
        Serializes the completion to a JSON string.

        Args:
            completion (TChatCompletion): The completion object from the client.

        Returns:
            str: The JSON string representation of the completion.
        """
        pass

    @abstractmethod
    def _extract_response(self, completion: TChatCompletion, schema: dict) -> Tuple[dict, TokenUsage, str]:
        """
        Extracts the response from the completion.

        Args:
            completion (TChatCompletion): The completion object from the client.
            schema (dict): The JSON schema for validation.

        Returns:
            Tuple[dict, TokenUsage, str]: A tuple containing the function arguments,
            token usage, and serialized completion.

        Raises:
            ExtractorValidationError: If validation fails.
            ExtractorError: For other extraction errors.
        """
        pass

    @abstractmethod
    def _get_messages(self, content: str) -> List[Dict[str, str]]:
        """
        Constructs the messages for the API call.

        Args:
            content (str): The user content.

        Returns:
            List[Dict[str, str]]: The list of message dictionaries.
        """
        pass

    @abstractmethod
    def execute(self, content: str, tool_call: ToolCall) -> Tuple[dict, TokenUsage, str]:
        """
        Executes the model with the given content and tool call.

        Args:
            content (str): The user content.
            tool_call (ToolCall): The tool call details.

        Returns:
            Tuple[dict, TokenUsage, str]: A tuple containing the function arguments,
            token usage, and serialized completion.
        """
        pass