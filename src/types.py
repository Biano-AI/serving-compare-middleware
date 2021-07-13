# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from enum import Enum, unique
from typing import BinaryIO, NamedTuple, Protocol

from httpx import AsyncClient


class ModelOutput(NamedTuple):
    class_name: str
    accuracy: float


class ModelInferenceCallbackProtocol(Protocol):
    async def __call__(self, client: AsyncClient, image_content: BinaryIO, url: str) -> ModelOutput:
        pass


@unique
class Servings(str, Enum):
    tfserving = "tfserving"
    torchserve = "torchserve"
    triton = "triton"
