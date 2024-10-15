from __future__ import annotations

from typing import Mapping

import httpx

from . import types
from ._base_client import DefaultAsyncHttpxClient, DefaultHttpxClient
from ._client import (
    AsyncClient,
    AsyncStream,
    AsyncTela,
    Client,
    RequestOptions,
    Stream,
    Tela,
    Timeout,
)
from ._constants import DEFAULT_CONNECTION_LIMITS, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from ._exceptions import (
    APIConnectionError,
    APIError,
    APIResponseValidationError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ContentFilterFinishReasonError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    TelaError,
    UnprocessableEntityError,
)
from ._models import BaseModel
from ._response import APIResponse as APIResponse
from ._response import AsyncAPIResponse as AsyncAPIResponse
from ._types import NOT_GIVEN, NoneType, NotGiven, ProxiesTypes
from ._utils._logs import setup_logging as _setup_logging
from ._version import __title__, __version__
from .resources import TelaFile, create_tela_file

__all__ = [
    "types",
    "__version__",
    "__title__",
    "NoneType",
    "ProxiesTypes",
    "NotGiven",
    "NOT_GIVEN",
    "TelaError",
    "APIError",
    "APIStatusError",
    "APITimeoutError",
    "APIConnectionError",
    "APIResponseValidationError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    "ContentFilterFinishReasonError",
    "Timeout",
    "RequestOptions",
    "Client",
    "AsyncClient",
    "Stream",
    "AsyncStream",
    "Tela",
    "AsyncTela",
    "BaseModel",
    "DEFAULT_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_CONNECTION_LIMITS",
    "DefaultHttpxClient",
    "DefaultAsyncHttpxClient",
    "TelaFile",
    "create_tela_file",
]

from .version import VERSION as VERSION

_setup_logging()

# Update the __module__ attribute for exported symbols so that
# error messages point to this module instead of the module
# it was originally defined in, e.g.
# tela._exceptions.NotFoundError -> tela.NotFoundError
__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        try:
            __locals[__name].__module__ = "tela"
        except (TypeError, AttributeError):
            # Some of our exported symbols are builtins which we can't set attributes for.
            pass


def create_tela_client(
    api_key: str | None = None,
    jwt: str | None = None,
    base_url: str | httpx.URL | None = None,
    timeout: float | Timeout | None = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_MAX_RETRIES,
    default_headers: Mapping[str, str] | None = None,
    default_query: Mapping[str, object] | None = None,
) -> Tela:
    return Tela(
        api_key=api_key,
        jwt=jwt,
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        default_headers=default_headers,
        default_query=default_query,
    )


def create_tela_async_client(
    api_key: str | None = None,
    jwt: str | None = None,
    base_url: str | httpx.URL | None = None,
    timeout: float | Timeout | None = DEFAULT_TIMEOUT,
    max_retries: int = DEFAULT_MAX_RETRIES,
    default_headers: Mapping[str, str] | None = None,
    default_query: Mapping[str, object] | None = None,
) -> AsyncTela:
    return AsyncTela(
        api_key=api_key,
        jwt=jwt,
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        default_headers=default_headers,
        default_query=default_query,
    )
