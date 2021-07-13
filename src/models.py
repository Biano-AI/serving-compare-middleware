# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import Final

from pydantic import BaseModel

logger: Final = logging.getLogger(__name__)


class FooOutputModel(BaseModel):
    """
    VSS req.

    """

    foo: str
