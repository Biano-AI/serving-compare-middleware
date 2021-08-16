# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import BinaryIO, Final

from httpx import AsyncClient

logger: Final = logging.getLogger(__name__)


async def torchserve_inference(client: AsyncClient, image_content: BinaryIO, url: str) -> None:
    response = await client.post(url, headers={"Content-Type": "image/jpeg"}, content=image_content.read())
    response.raise_for_status()
