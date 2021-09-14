# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    tfserving_service_url: AnyUrl
    torchserve_service_url: AnyUrl
    triton_service_host: str

    tfserving_grpc_host: str = "localhost:9000"
    torchserve_grpc_host: str = "localhost:7070"
    triton_grpc_host: str = "localhost:XXXX"

    class Config:
        env_file = ".env"
