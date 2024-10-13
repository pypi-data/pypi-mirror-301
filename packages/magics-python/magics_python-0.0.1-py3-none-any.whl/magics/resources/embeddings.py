from __future__ import annotations

from typing import List, Any

from magics.abstract import api_requestor
from magics.magics_response import MagicsResponse
from magics.types import (
    EmbeddingRequest,
    EmbeddingResponse,
    MagicsClient,
    MagicsRequest,
)


class Embeddings:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    def create(
        self,
        *,
        input: str | List[str],
        model: str,
        **kwargs: Any,
    ) -> EmbeddingResponse:
        """
        Method to generate completions based on a given prompt using a specified model.

        Args:
            input (str | List[str]): A string or list of strings to embed
            model (str): The name of the model to query.

        Returns:
            EmbeddingResponse: Object containing embeddings
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="POST",
                url="embeddings",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return EmbeddingResponse(**response.data)


class AsyncEmbeddings:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        input: str | List[str],
        model: str,
        **kwargs: Any,
    ) -> EmbeddingResponse:
        """
        Async method to generate completions based on a given prompt using a specified model.

        Args:
            input (str | List[str]): A string or list of strings to embed
            model (str): The name of the model to query.

        Returns:
            EmbeddingResponse: Object containing embeddings
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, _, _ = await requestor.arequest(
            options=MagicsRequest(
                method="POST",
                url="embeddings",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return EmbeddingResponse(**response.data)
