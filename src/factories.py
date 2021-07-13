# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final

import httpx

logger: Final = logging.getLogger(__name__)


async def make_httpx_client():
    return httpx.AsyncClient()
