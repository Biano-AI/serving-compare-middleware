# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from functools import cache
from typing import Final

import httpx
from src.dependencies import get_settings

try:
    from tritonclient.http import InferenceServerClient
except ImportError:
    InferenceServerClient = object()

logger: Final = logging.getLogger(__name__)


async def make_httpx_client():
    return httpx.AsyncClient(timeout=10.0)


@cache
def make_triton_client() -> InferenceServerClient:
    from tritonclient.http import InferenceServerClient
    return InferenceServerClient(url=get_settings().triton_service_host)
