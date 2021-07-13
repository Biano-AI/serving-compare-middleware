# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import io
import logging
from typing import cast, Final

import httpx
from fastapi import APIRouter, Depends, File, UploadFile

from src.dependencies import httpx_client
from src.inference import AVAILABLE_SERVINGS
from src.models import FooOutputModel
from src.types import Servings

logger: Final = logging.getLogger(__name__)
router: Final = APIRouter()


@router.post(
    "/infer/{model_name}",
    response_model=FooOutputModel,
    summary="TBD",
)
async def _(
    *,
    model_name: Servings,
    client: httpx.AsyncClient = Depends(httpx_client),
    image: UploadFile = File(...),
) -> FooOutputModel:
    """
    TBD
    """
    image_content = io.BytesIO(cast(bytes, await image.read()))
    inference_function, service_url = AVAILABLE_SERVINGS[model_name]

    await inference_function(client=client, image_content=image_content, url=service_url)

    return FooOutputModel(foo="bar")
