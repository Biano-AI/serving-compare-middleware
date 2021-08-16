# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    tfserving_service_url: AnyUrl
    torchserve_service_url: AnyUrl
    triton_service_host: str

    class Config:
        env_file = ".env"
