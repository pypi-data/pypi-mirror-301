import warnings
from typing import Any, Dict

import magics
from magics.legacy.base import API_KEY_WARNING, deprecated


class Image:
    @classmethod
    @deprecated  # type: ignore
    def create(
        cls,
        prompt: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Legacy image function."""

        api_key = None
        if magics.api_key:
            warnings.warn(API_KEY_WARNING)
            api_key = magics.api_key

        client = magics.Magics(api_key=api_key)

        return client.images.generate(prompt=prompt, **kwargs).model_dump(
            exclude_none=True
        )
