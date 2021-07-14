# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging
from typing import BinaryIO, Final

import numpy as np
from tritonclient.http import InferInput, InferRequestedOutput

from src.factories import make_triton_client

logger: Final = logging.getLogger(__name__)


async def triton_tensorflow_inference(image_content: BinaryIO, **kwargs):
    triton_client = make_triton_client()

    # TODO Convert image_content to the model input
    embeddings = np.empty([42, 42])

    infer_input = InferInput("input__0", [1, 1536], "FP32")
    infer_input.set_data_from_numpy(embeddings)
    output = InferRequestedOutput("output__0")
    response = triton_client.infer("some model name", model_version=42, inputs=[infer_input], outputs=[output])

    response.as_numpy("output__0").tolist()


async def triton_pytorch_inference(image_content: BinaryIO, **kwargs):
    triton_client = make_triton_client()

    # TODO Convert image_content to the model input
    embeddings = np.empty([42, 42])

    infer_input = InferInput("input__0", [1, 1536], "FP32")
    infer_input.set_data_from_numpy(embeddings)
    output = InferRequestedOutput("output__0")
    response = triton_client.infer("some model name", model_version=42, inputs=[infer_input], outputs=[output])

    response.as_numpy("output__0").tolist()
