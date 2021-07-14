# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import io
import logging
from typing import cast, Final

import httpx
from fastapi import APIRouter, Depends, File, UploadFile
from starlette.responses import PlainTextResponse

from src.dependencies import httpx_client
from src.inference import AVAILABLE_SERVINGS
from src.types import Servings

logger: Final = logging.getLogger(__name__)
router: Final = APIRouter()


@router.post(
    "/infer/{model_name}",
    response_model=PlainTextResponse,
    summary="TBD",
)
async def _(
    *,
    model_name: Servings,
    client: httpx.AsyncClient = Depends(httpx_client),
    image: UploadFile = File(...),
) -> str:
    """
    TBD
    """
    image_content = io.BytesIO(cast(bytes, await image.read()))
    inference_function, service_url = AVAILABLE_SERVINGS[model_name]

    await inference_function(client=client, image_content=image_content, url=service_url)

    return "OK"
