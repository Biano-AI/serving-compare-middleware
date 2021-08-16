# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import functools
import logging
import os
import random
from pathlib import Path
from typing import Final, List

import httpx
from starlette.requests import Request

from src.config import Settings

logger: Final = logging.getLogger(__name__)


def httpx_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.httpx_client


@functools.cache
def datadir() -> Path:
    if DATA_DIR := os.environ.get("DATA_DIR"):
        return Path(DATA_DIR).resolve(strict=True)
    else:
        return Path.cwd() / "data"


@functools.cache
def images_in_datadir() -> List[Path]:
    return list((datadir() / "imagenet").glob("*.JPEG"))


def get_random_image() -> Path:
    return random.choice(images_in_datadir())


@functools.cache
def get_settings() -> Settings:
    return Settings()
