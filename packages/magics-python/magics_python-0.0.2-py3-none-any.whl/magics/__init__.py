from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable

from magics import (
    abstract,
    client,
    constants,
    error,
    filemanager,
    resources,
    magics_response,
    types,
    utils,
)
from magics.version import VERSION

from magics.legacy.complete import AsyncComplete, Complete, Completion
from magics.legacy.embeddings import Embeddings
from magics.legacy.files import Files
from magics.legacy.finetune import Finetune
from magics.legacy.images import Image
from magics.legacy.models import Models

version = VERSION

log: str | None = None  # Set to either 'debug' or 'info', controls console logging

if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

requestssession: "requests.Session" | Callable[[], "requests.Session"] | None = None

aiosession: ContextVar["ClientSession" | None] = ContextVar(
    "aiohttp-session", default=None
)

from magics.client import AsyncClient, AsyncMagics, Client, Magics


api_key: str | None = None  # To be deprecated in the next major release

# Legacy functions


__all__ = [
    "aiosession",
    "constants",
    "version",
    "Magics",
    "AsyncMagics",
    "Client",
    "AsyncClient",
    "resources",
    "types",
    "abstract",
    "filemanager",
    "error",
    "magics_response",
    "client",
    "utils",
    "Complete",
    "AsyncComplete",
    "Completion",
    "Embeddings",
    "Files",
    "Finetune",
    "Image",
    "Models",
]
