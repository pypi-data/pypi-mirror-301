from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional

import httpx
from typing_extensions import Literal, cast, overload

from ..._base_client import make_request_options
from ..._exceptions import FileUploadError
from ..._models import BaseModel
from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._streaming import AsyncStream, Stream
from ..._types import NOT_GIVEN, Headers, NotGiven
from ..._utils import async_maybe_transform, maybe_transform, required_args
from ...types.chat.chat_completion import (
    ChatCompletionCreateResponse,
    ChatCompletionCreateResponseStream,
    ChatCompletionWebhookResponse,
)
from ...types.chat.chat_completion_file import TelaFile, create_tela_file
from ...types.chat.chat_completions_create_param import (
    ChatCompletionCreateMessagesParam,
    ChatCompletionCreateOverrideParams,
    CompletionCreateParams,
)

__all__ = ["Completions", "AsyncCompletions", "TelaFile", "create_tela_file"]


class Completions(SyncAPIResource):
    """
    Manages chat completion operations.

    Provides methods to create chat completions, handle streaming responses,
    and manage file uploads associated with chat completions.

    @example
    ```python
    tela = create_tela_client(api_key="your-api-key")
    response = tela.completions.create(
        canvas_id="your-canvas-id",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(response.choices[0].message.content)
    ```
    """

    @overload
    def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: str,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionWebhookResponse: ...

    @overload
    def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: Optional[NotGiven] = NOT_GIVEN,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse: ...

    @overload
    def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: Optional[NotGiven] = NOT_GIVEN,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Literal[True],
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[ChatCompletionCreateResponseStream]: ...

    @required_args(["canvas_id"], ["application_id"])
    def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: Optional[str] | NotGiven = NOT_GIVEN,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse | Stream[ChatCompletionCreateResponseStream] | ChatCompletionWebhookResponse:
        """
        Creates a chat completion with various input options and response formats.

        This method supports synchronous responses, streaming responses, and webhook-based asynchronous processing.

        Args:
            canvas_id (Optional[str] | NotGiven): The ID of the canvas.
            application_id (Optional[str] | NotGiven): The ID of the application.
            webhook_url (Optional[str] | NotGiven): The webhook URL for asynchronous responses.
            variables (Optional[Dict[str, str | TelaFile]] | NotGiven): Variables for the chat completion.
            messages (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven): The chat messages.
            override (Optional[ChatCompletionCreateOverrideParams] | NotGiven): Override parameters.
            stream (Optional[Literal[False]] | Literal[True] | NotGiven): Whether to stream the response.
            extra_headers (Headers | None): Additional headers for the request.
            timeout (float | httpx.Timeout | None | NotGiven): Timeout for the request.

        Returns:
            ChatCompletionCreateResponse | Stream[ChatCompletionCreateResponseStream] | ChatCompletionWebhookResponse

        @example
        ```python
        # Synchronous response
        response = tela.completions.create(
            canvas_id="your-canvas-id",
            messages=[{"role": "user", "content": "Tell me a joke."}],
        )

        # Streaming response
        stream = tela.completions.create(
            canvas_id="your-canvas-id",
            messages=[{"role": "user", "content": "Tell me a story."}],
            stream=True,
        )

        # Webhook response
        webhook_response = tela.completions.create(
            canvas_id="your-canvas-id",
            messages=[{"role": "user", "content": "Generate a report."}],
            webhook_url="https://example.com/webhook",
        )

        # File upload example
        with open("path/to/sample-invoice.pdf", "rb") as f:
            file = create_tela_file(f)
            completion = tela.completions.create(
                canvas_id="your-canvas-id",
                variables={
                    "document": file,
                },
            )
            print(completion.choices[0].message.content)
        ```
        """
        class_casting = (
            ChatCompletionCreateResponse
            if type(webhook_url) is NotGiven or webhook_url is None
            else ChatCompletionWebhookResponse
        )
        processed_variables = variables
        if variables is not NOT_GIVEN and variables is not None:
            processed_variables = {}
            for (
                key,
                value,
            ) in variables.items():  # pyright: ignore[reportAttributeAccessIssue]
                if isinstance(value, TelaFile):
                    file_with_url = self._upload_file(value)
                    processed_variables[key] = file_with_url
                else:
                    processed_variables[key] = value

        return self._post(
            "/v2/chat/completions",
            body=maybe_transform(
                {
                    "canvas_id": canvas_id,
                    "application_id": application_id,
                    "webhook_url": webhook_url,
                    "variables": processed_variables,
                    "override": override,
                    "messages": messages,
                    "stream": stream,
                },
                CompletionCreateParams,
            ),
            options=make_request_options(extra_headers=extra_headers, timeout=timeout),
            cast_to=class_casting,
            stream=stream or False,
            stream_cls=Stream[ChatCompletionCreateResponseStream],
        )

    def _upload_file(self, file: TelaFile) -> Dict[str, Any]:
        """
        Uploads a file and returns its URL and options.

        This is used internally to handle file uploads associated with chat completions.

        Args:
            file (TelaFile): The file to be uploaded.

        Returns:
            Dict[str, Any]: A dictionary containing the file URL and options.

        Raises:
            FileUploadError: If the file upload fails.
        """
        content = file.get_uploadable_content()

        if file.is_url and isinstance(content, str):
            return {"file_url": content, "options": file.options}

        class FileUploadResponse(BaseModel):
            upload_url: str
            download_url: str

        response = self._post("/v2/file", cast_to=FileUploadResponse)
        upload_url, download_url = response.uploadUrl, response.downloadUrl

        headers = {
            "Content-Type": file.content_type,
        }
        if file.size:
            headers["Content-Length"] = str(file.size)

        try:
            upload_response = httpx.put(upload_url, content=content, headers=cast(Mapping[str, str], headers))
            upload_response.raise_for_status()
        except Exception as e:
            raise FileUploadError() from e

        return {"file_url": download_url, "options": file.options}


class AsyncCompletions(AsyncAPIResource):
    """
    Manages asynchronous chat completion operations.

    Provides asynchronous methods to create chat completions, handle streaming responses,
    and manage file uploads associated with chat completions.

    @example
    ```python
    tela = create_async_tela_client(api_key="your-api-key")
    response = await tela.completions.create(
        canvas_id="your-canvas-id",
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(response.choices[0].message.content)
    ```
    """

    @overload
    async def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: str,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionWebhookResponse: ...

    @overload
    async def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: Optional[NotGiven] = NOT_GIVEN,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse: ...

    @overload
    async def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: Optional[NotGiven] = NOT_GIVEN,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Literal[True],
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[ChatCompletionCreateResponseStream]: ...

    @required_args(["canvas_id"], ["application_id"])
    async def create(
        self,
        *,
        canvas_id: Optional[str] | NotGiven = NOT_GIVEN,
        application_id: Optional[str] | NotGiven = NOT_GIVEN,
        webhook_url: Optional[str] | NotGiven = NOT_GIVEN,
        variables: Optional[Dict[str, str | TelaFile]] | NotGiven = NOT_GIVEN,
        messages: (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven) = NOT_GIVEN,
        override: Optional[ChatCompletionCreateOverrideParams] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse | AsyncStream[ChatCompletionCreateResponseStream] | ChatCompletionWebhookResponse:
        """
        Creates a chat completion with various input options and response formats asynchronously.

        This method supports synchronous responses, streaming responses, and webhook-based asynchronous processing.

        Args:
            canvas_id (Optional[str] | NotGiven): The ID of the canvas.
            application_id (Optional[str] | NotGiven): The ID of the application.
            webhook_url (Optional[str] | NotGiven): The webhook URL for asynchronous responses.
            variables (Optional[Dict[str, str | TelaFile]] | NotGiven): Variables for the chat completion.
            messages (Optional[Iterable[ChatCompletionCreateMessagesParam]] | NotGiven): The chat messages.
            override (Optional[ChatCompletionCreateOverrideParams] | NotGiven): Override parameters.
            stream (Optional[Literal[False]] | Literal[True] | NotGiven): Whether to stream the response.
            extra_headers (Headers | None): Additional headers for the request.
            timeout (float | httpx.Timeout | None | NotGiven): Timeout for the request.

        Returns:
            ChatCompletionCreateResponse | AsyncStream[ChatCompletionCreateResponseStream] | ChatCompletionWebhookResponse:

        @example
        ```python
        # Synchronous response
        response = await tela.completions.create(
            canvas_id="your-canvas-id",
            messages=[{"role": "user", "content": "Tell me a joke."}],
        )

        # Streaming response
        stream = await tela.completions.create(
            canvas_id="your-canvas-id",
            messages=[{"role": "user", "content": "Tell me a story."}],
            stream=True,
        )

        # Webhook response
        webhook_response = await tela.completions.create(
            canvas_id="your-canvas-id",
            messages=[{"role": "user", "content": "Generate a report."}],
            webhook_url="https://example.com/webhook",
        )

        # File upload example
        with open("path/to/sample-invoice.pdf", "rb") as f:
            file = create_tela_file(f)
            completion = await tela.completions.create(
                canvas_id="your-canvas-id",
                variables={
                    "document": file,
                },
            )
            print(completion.choices[0].message.content)
        ```
        """
        class_casting = (
            ChatCompletionCreateResponse
            if type(webhook_url) is NotGiven or webhook_url is None
            else ChatCompletionWebhookResponse
        )
        processed_variables = variables
        if variables is not NOT_GIVEN and variables is not None:
            processed_variables = {}
            for (
                key,
                value,
            ) in variables.items():  # pyright: ignore[reportAttributeAccessIssue]
                if isinstance(value, TelaFile):
                    file_with_url = await self._upload_file(value)
                    processed_variables[key] = file_with_url
                else:
                    processed_variables[key] = value

        return await self._post(
            "/v2/chat/completions",
            body=await async_maybe_transform(
                {
                    "canvas_id": canvas_id,
                    "application_id": application_id,
                    "webhook_url": webhook_url,
                    "variables": processed_variables,
                    "override": override,
                    "messages": messages,
                    "stream": stream,
                },
                CompletionCreateParams,
            ),
            options=make_request_options(extra_headers=extra_headers, timeout=timeout),
            cast_to=class_casting,
            stream=stream or False,
            stream_cls=AsyncStream[ChatCompletionCreateResponseStream],
        )

    async def _upload_file(self, file: TelaFile) -> Dict[str, Any]:
        """
        Uploads a file and returns its URL and options asynchronously.

        This is used internally to handle file uploads associated with chat completions.

        Args:
            file (TelaFile): The file to be uploaded.

        Returns:
            Dict[str, Any]: A dictionary containing the file URL and options.

        Raises:
            FileUploadError: If the file upload fails.
        """
        content = file.get_uploadable_content()

        if file.is_url and isinstance(content, str):
            return {"file_url": content, "options": file.options}

        class FileUploadResponse(BaseModel):
            upload_url: str
            download_url: str

        response = await self._post("/v2/file", cast_to=FileUploadResponse)
        upload_url, download_url = response.uploadUrl, response.downloadUrl

        headers = {
            "Content-Type": file.content_type,
        }
        if file.size:
            headers["Content-Length"] = str(file.size)

        try:
            upload_response = await httpx.AsyncClient().put(
                upload_url, content=content, headers=cast(Mapping[str, str], headers)
            )
            upload_response.raise_for_status()
        except Exception as e:
            raise FileUploadError() from e

        return {"file_url": download_url, "options": file.options}
