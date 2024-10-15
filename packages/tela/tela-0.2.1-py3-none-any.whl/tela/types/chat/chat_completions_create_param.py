from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from typing_extensions import Literal, Required, TypedDict

from ..._types import NotGiven

__all__ = [
    "ChatCompletionVariablesWithFileURL",
    "ChatCompletionCreateMessagesParam",
    "ChatCompletionCreateOverrideFunctionParameters",
    "ChatCompletionCreateOverrideFunction",
    "ChatCompletionCreateOverrideStructuredOutputSchema",
    "ChatCompletionCreateOverrideStructuredOutput",
    "ChatCompletionCreateOverrideParams",
    "ChatCompletionCreateParamsBase",
    "ChatCompletionCreateParamsStreaming",
    "ChatCompletionCreateParamsNonStreaming",
    "ChatCompletionCreateWebhookParams",
    "CompletionCreateParams",
]

ChatCompletionVariablesWithFileURL = Dict[str, Union[str, int, bool, Dict[Literal["file_url"], str]]]


class ChatCompletionCreateMessagesParam(TypedDict, total=False):
    """Represents a message in the chat conversation."""

    role: Required[Literal["system", "user", "assistant", "tool"]]
    """ The role of the message sender."""

    content: Required[str]
    """ The content of the message."""


class ChatCompletionCreateOverrideFunctionParameters(TypedDict, total=False):
    """Parameters for overriding a function in the chat completion."""

    type: Required[Literal["object"]]
    """ The type of override; must be 'object'."""
    properties: Required[Dict[str, Any]]
    """ The properties of the override."""
    required: Optional[List[str]]
    """ A list of required properties."""


class ChatCompletionCreateOverrideFunction(TypedDict, total=False):
    """Defines a function that can be overridden in the chat completion."""

    id: Required[str]
    """ The unique identifier of the function."""
    name: Required[str]
    """ The name of the function."""
    description: Optional[str]
    """ A description of the function."""
    parameters: Optional[ChatCompletionCreateOverrideFunctionParameters]
    """ The parameters for the function."""


class ChatCompletionCreateOverrideStructuredOutputSchema(TypedDict, total=False):
    """Defines the schema for structured output in the chat completion."""

    properties: Required[Dict[str, Any]]
    """ The properties of the schema."""
    type: Required[Literal["object"]]
    """ The type of the schema; must be 'object'."""
    title: Required[str]
    """ The title of the schema."""
    description: Required[str]
    """ A description of the schema."""
    required: Optional[List[str]]
    """ A list of required properties."""


class ChatCompletionCreateOverrideStructuredOutput(TypedDict, total=False):
    """Configuration for generating structured output in the chat completion."""

    enabled: Required[bool]
    """ Whether to enable structured output."""
    schema: Optional[ChatCompletionCreateOverrideStructuredOutputSchema]
    """ The schema defining the structure of the output."""


class ChatCompletionCreateOverrideParams(TypedDict, total=False):
    """Override parameters for customizing the chat completion behavior."""

    model: Optional[str]
    """ The specific model to use for this completion."""
    temperature: Optional[float]
    """ Controls randomness in the output. Values between 0 and 1."""
    type: Required[Literal["chat", "completion"]]
    """ Specifies whether to use a chat or completion model."""
    functions: Optional[List[ChatCompletionCreateOverrideFunction]]
    """ An array of functions that the model can call."""
    structured_output: Optional[ChatCompletionCreateOverrideStructuredOutput]
    """ Configuration for generating structured output."""


class ChatCompletionCreateParamsBase(TypedDict, total=False):
    """Base parameters for creating a chat completion."""

    canvas_id: Optional[str]
    """ The ID of the canvas to use for this chat completion."""
    application_id: Optional[str]
    """ The ID of the deployed application to use for this chat completion."""
    override: Optional[ChatCompletionCreateOverrideParams]
    """ Override default settings specified in the canvas."""
    messages: Optional[List[ChatCompletionCreateMessagesParam]]
    """ An array of previous messages in the conversation."""


class ChatCompletionCreateParamsStreaming(ChatCompletionCreateParamsBase):
    """Parameters for creating a streaming chat completion."""

    stream: Required[Literal[True]]
    """ Indicates that the response should be streamed."""


class ChatCompletionCreateParamsNonStreaming(ChatCompletionCreateParamsBase):
    """Parameters for creating a non-streaming chat completion."""

    stream: Required[Union[Literal[False], NotGiven, None]]
    """ Indicates that the response should not be streamed."""


class ChatCompletionCreateWebhookParams(ChatCompletionCreateParamsBase):
    """Parameters for creating a chat completion with a webhook."""

    webhook_url: Required[str]
    """ The webhook URL to receive a notification when the chat completion is finished."""


CompletionCreateParams = Union[
    ChatCompletionCreateParamsNonStreaming,
    ChatCompletionCreateParamsStreaming,
    ChatCompletionCreateWebhookParams,
]
