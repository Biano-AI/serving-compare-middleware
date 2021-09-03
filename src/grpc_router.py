# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import io
import logging
from pathlib import Path
from typing import cast, Final

import aiofiles
import httpx
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import PlainTextResponse

from src.dependencies import get_random_image, httpx_client
from src.inference import AVAILABLE_SERVINGS
from src.types import Servings

logger: Final = logging.getLogger(__name__)
router: Final = APIRouter()


@router.post(
    "/infer/{serving_type}",
    response_class=PlainTextResponse,
    summary="Performs GRPC inference for an image",
)
async def _(
    *,
    serving_type: Servings,
    client: httpx.AsyncClient = Depends(httpx_client),
    image: UploadFile = File(...),
) -> str:
    """
    Performs inference for the input image (JPEG).
    Based on the value of `serving_type`, it selects the correct
    backend implementation for the model and calls this backend.

    The output of the model is discarded.
    """
    image_content = io.BytesIO(cast(bytes, await image.read()))
    inference_function, service_url = AVAILABLE_SERVINGS[serving_type]

    await inference_function(client=client, image_content=image_content, url=service_url)

    return "OK"


@router.get(
    "/randinfer/{serving_type}",
    response_class=PlainTextResponse,
    summary="Performs GRPC inference for an image",
)
async def _(
    *,
    serving_type: Servings,
    random_image: Path = Depends(get_random_image),
    client: httpx.AsyncClient = Depends(httpx_client),
) -> str:
    """
    Performs inference for the input image (JPEG).
    Based on the value of `serving_type`, it selects the correct
    backend implementation for the model and calls this backend.

    The output of the model is discarded.
    """

    async with aiofiles.open(random_image, mode="rb") as f:
        image_content = io.BytesIO(await f.read())

    inference_function, service_url = AVAILABLE_SERVINGS[serving_type]

    await inference_function(client=client, image_content=image_content, url=service_url)

    return "OK"
