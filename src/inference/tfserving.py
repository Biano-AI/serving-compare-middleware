# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import BinaryIO, Final

import numpy as np
from httpx import AsyncClient
from PIL import Image

logger: Final = logging.getLogger(__name__)


async def tfserving_inference(client: AsyncClient, image_content: BinaryIO, url: str) -> None:
    """
    Source:
        https://raw.githubusercontent.com/tensorflow/serving/master/tensorflow_serving/example/resnet_client.py
    """
    jpeg_rgb = Image.open(image_content).convert("RGB")
    jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).tolist()

    response = await client.post(url, json={"instances": jpeg_rgb})
    response.raise_for_status()
