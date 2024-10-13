from base64 import b64decode
from datetime import datetime, timedelta
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests


class APIResponse:
    def __init__(self, response: dict) -> None:
        self.response = response

    @property
    def data(self) -> bytes:
        if data := self.response.get("image_data"):
            return b64decode(data)

        if self.url:
            response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})

            if response.ok:
                return response.content

            response.raise_for_status()

        return None

    @property
    def image(self) -> object:
        try:
            from PIL import Image
        except ImportError as e:
            raise ImportError('Pillow package is not installed. Please install it using "pip install pillow"') from e

        return Image.open(BytesIO(self.data))

    @property
    def url(self) -> str:
        return self.response.get("image_url")

    @property
    def seed(self) -> Optional[int]:
        return self.response.get("seed")

    @property
    def mime_type(self) -> Optional[str]:
        return self.response.get("mime_type")

    @property
    def duration(self) -> Optional[timedelta]:
        if (started_at := self.response.get("started_at")) and (completed_at := self.response.get("completed_at")):
            return datetime.fromisoformat(completed_at) - datetime.fromisoformat(started_at)

        return None

    def save(self, path: str) -> None:
        with Path(path).open("wb") as f:
            f.write(self.data)


class ImagePig:
    """
    Image Pig API
    https://imagepig.com/docs/
    """

    class Proportion(Enum):
        LANDSCAPE = "landscape"
        PORTRAIT = "portrait"
        SQUARE = "square"
        WIDE = "wide"

    def __init__(self, api_key: str, api_url: str = "https://api.imagepig.com") -> None:
        self.api_key = api_key
        self.api_url = api_url

    def _api_call(self, endpoint: str, payload: dict) -> APIResponse:
        response = requests.post(
            f"{self.api_url}/{endpoint}",
            headers={"Api-Key": self.api_key},
            json=payload,
        )

        if response.ok:
            return APIResponse(response.json())

        response.raise_for_status()

    def _check_url(self, url: str) -> None:
        parsed_url = urlparse(url)
        assert parsed_url.scheme in {"http", "https"} and parsed_url.netloc

    def default(self, prompt: str, negative_prompt: str = "", **kwargs) -> APIResponse:
        kwargs.update({"positive_prompt": prompt, "negative_prompt": prompt})
        return self._api_call("", kwargs)

    def xl(self, prompt: str, negative_prompt: str = "", **kwargs) -> APIResponse:
        kwargs.update({"positive_prompt": prompt, "negative_prompt": prompt})
        return self._api_call("xl", kwargs)

    def flux(self, prompt: str, proportion: Proportion = Proportion.LANDSCAPE, **kwargs) -> APIResponse:
        kwargs.update({"positive_prompt": prompt, "proportion": proportion.value})
        return self._api_call("flux", kwargs)

    def faceswap(self, source_image_url: str, target_image_url: str, **kwargs) -> APIResponse:
        self._check_url(source_image_url)
        self._check_url(target_image_url)
        kwargs.update({"source_image_url": source_image_url, "target_image_url": target_image_url})
        return self._api_call("faceswap", kwargs)
