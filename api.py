# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final

from fastapi import FastAPI

from src import common_router, factories

logger: Final = logging.getLogger(__name__)

main = FastAPI(title="TBD", description="TBD | Biano AI", version="0.1.0", redoc_url=None)
main.include_router(common_router.router, tags=["inference"])


@main.on_event("startup")
async def make_client_sessions():
    logger.info("STARTUP: Making HTTPX Client")
    session = await factories.make_httpx_client()
    setattr(main.state, "httpx_client", session)


@main.on_event("shutdown")
async def close_client_sessions():
    logger.info("SHUTDOWN: Closing HTTPX Client")
    await main.state.httpx_client.aclose()
