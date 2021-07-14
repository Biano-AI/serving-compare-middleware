# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from enum import Enum, unique
from typing import BinaryIO, Protocol

from httpx import AsyncClient


class ModelInferenceCallbackProtocol(Protocol):
    async def __call__(self, client: AsyncClient, image_content: BinaryIO, url: str) -> None:
        pass


@unique
class Servings(str, Enum):
    tfserving = "tfserving"
    torchserve = "torchserve"
    triton = "triton"
