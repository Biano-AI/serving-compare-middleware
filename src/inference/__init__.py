# -*- encoding: utf-8 -*-
# ! python3

from typing import Dict, Final, Tuple

from pydantic import AnyUrl

from .tfserving import tfserving_inference
from .torchserve import torchserve_inference
from .triton import triton_pytorch_inference, triton_tensorflow_inference
from ..dependencies import get_settings
from ..types import ModelInferenceCallbackProtocol, Servings

AVAILABLE_SERVINGS: Final[Dict[Servings, Tuple[ModelInferenceCallbackProtocol, AnyUrl]]] = {
    Servings.tfserving: (tfserving_inference, get_settings().tfserving_service_url),
    Servings.torchserve: (torchserve_inference, get_settings().torchserve_service_url),
    Servings.triton_tensorflow: (triton_tensorflow_inference, get_settings().triton_service_url),
    Servings.triton_pytorch: (triton_pytorch_inference, get_settings().triton_service_url),
}

__all__ = ("AVAILABLE_SERVINGS",)
