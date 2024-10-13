from __future__ import annotations

from typing import List

from magics.abstract import api_requestor
from magics.magics_response import MagicsResponse
from magics.types import (
    ModelObject,
    MagicsClient,
    MagicsRequest,
)


class Models:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    def list(
        self,
    ) -> List[ModelObject]:
        """
        Method to return list of models on the API

        Returns:
            List[ModelObject]: List of model objects
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)
        assert isinstance(response.data, list)
        # print(response.data[0])
        return [ModelObject(**model) for model in response.data]


class AsyncModels:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    async def list(
        self,
    ) -> List[ModelObject]:
        """
        Async method to return list of models on API

        Returns:
            List[ModelObject]: List of model objects
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=MagicsRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)
        assert isinstance(response.data, list)

        return [ModelObject(**model) for model in response.data]
