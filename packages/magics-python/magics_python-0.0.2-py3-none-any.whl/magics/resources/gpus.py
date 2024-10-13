from __future__ import annotations

import time
from typing import AsyncGenerator, Dict, Iterator, List, Any

from magics.abstract import api_requestor
from magics.magics_response import MagicsResponse
from magics.types import (
    CompletionChunk,
    CompletionRequest,
    CompletionResponse,
    MagicsClient,
    MagicsRequest,
    PrivateLLMResource,
)
from magics.types.resources import GpuResource as GpuResource_


class GpuResource:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    def list(self):
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="POST",
                url="resources/gpus",
            ),
        )
        assert isinstance(response, MagicsResponse)
        # print(response.data)
        return [GpuResource_(**gpu) for gpu in response.data]
