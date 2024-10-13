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
    PrivateLLMResource
)
from magics.types.resources import EmptyResourcesRequest, LLMResourcesRequest, PrivateEmptyResource, ResourceDeleteRequest



class Resources:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    def request(self, resource):
        if isinstance(resource, LLMResourcesRequest):
            requestor = api_requestor.APIRequestor(
                client=self._client,
            )

            parameter_payload = resource.model_dump(exclude_none=True)

            response, _, _ = requestor.request(
                options=MagicsRequest(
                    method="POST",
                    url="resources/request/llm",
                    params=parameter_payload,
                ),
            )
            assert isinstance(response, MagicsResponse)
            # print(response.data)
            return PrivateLLMResource(**response.data)
        elif isinstance(resource, EmptyResourcesRequest):
            requestor = api_requestor.APIRequestor(
                client=self._client,
            )

            parameter_payload = resource.model_dump(exclude_none=True)

            response, _, _ = requestor.request(
                options=MagicsRequest(
                    method="POST",
                    url="resources/request/empty",
                    params=parameter_payload,
                ),
            )
            assert isinstance(response, MagicsResponse)
            return PrivateEmptyResource(**response.data)


    def delete(self, resource: PrivateLLMResource | PrivateEmptyResource):
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        resource = ResourceDeleteRequest(resource_id=resource.resource_id)
        parameter_payload = resource.model_dump(exclude_none=True)
        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="POST",
                url=f"resources/delete",
                params=parameter_payload,
            ),
        )
        assert isinstance(response, MagicsResponse)
        return response.data
    
    def ready(self, resource: PrivateLLMResource):
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        parameter_payload = resource.model_dump(exclude_none=True)
        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="POST",
                url=f"resources/ready/llm",
                params=parameter_payload,
            ),
        )
        assert isinstance(response, MagicsResponse)
        print(response.data)
        if response.data.get('status') == 'ok':
            return True
        else:
            return False
    
    def wait(self, resource: PrivateLLMResource, seconds: int = 30):
        for _ in range(seconds):
            if self.ready(resource):
                return True
            time.sleep(1)
        return False
    