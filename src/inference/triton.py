# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from pprint import pprint
from typing import BinaryIO, Final

from httpx import AsyncClient

from src.types import ModelOutput

logger: Final = logging.getLogger(__name__)


async def triton_inference(client: AsyncClient, image_content: BinaryIO, url: str) -> ModelOutput:
    pprint(image_content)
    # TODO Implement me
    raise NotImplementedError()
