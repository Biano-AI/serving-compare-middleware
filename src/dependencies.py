# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import functools

import httpx
from starlette.requests import Request

from src.config import Settings


def httpx_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.httpx_client


@functools.cache
def get_settings() -> Settings:
    return Settings()
