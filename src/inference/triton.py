# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
import platform
from typing import BinaryIO, Final

import numpy as np
from PIL import Image

from src.factories import make_triton_http_client

logger: Final = logging.getLogger(__name__)

try:
    from tritonclient.http import InferInput, InferRequestedOutput
except ImportError as e:
    if platform.system() == "Windows":
        logger.warning(
            "Triton is not available on Windows. "
            "Inference will not work on this server, "
            "but at least the whole project will run."
        )
        InferInput = object()
        InferRequestedOutput = object()
    else:
        raise RuntimeError("Failed to import Triton client") from e


async def triton_tensorflow_inference(image_content: BinaryIO, **kwargs):
    triton_client = make_triton_http_client()

    jpeg_rgb = Image.open(image_content).convert("RGB")
    jpeg_rgb = jpeg_rgb.resize((224, 224))
    jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).astype(np.float32)

    infer_input = InferInput("input_1", [1, 224, 224, 3], "FP32")
    infer_input.set_data_from_numpy(jpeg_rgb)
    output = InferRequestedOutput("activation_49")
    response = triton_client.infer("resnet-50-tensorflow", model_version="1", inputs=[infer_input], outputs=[output])

    assert response.as_numpy("activation_49").tolist()


async def triton_pytorch_inference(image_content: BinaryIO, **kwargs):
    triton_client = make_triton_http_client()

    jpeg_rgb = Image.open(image_content).convert("RGB")
    jpeg_rgb = jpeg_rgb.resize((224, 224))
    normalized_jpeg = (np.array(jpeg_rgb) - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
    normalized_jpeg = np.expand_dims(np.einsum("ijk->kij", np.array(normalized_jpeg)), 0).astype(np.float32)

    infer_input = InferInput("input__0", [1, 3, 224, 224], "FP32")
    infer_input.set_data_from_numpy(normalized_jpeg)
    output = InferRequestedOutput("output__0")
    response = triton_client.infer("resnet-50-torch", model_version="1", inputs=[infer_input], outputs=[output])

    assert response.as_numpy("output__0").tolist()
