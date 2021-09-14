# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import io
import logging
from pathlib import Path
import platform
from typing import BinaryIO, cast, Final

import aiofiles
import grpc
import httpx
import numpy as np
from devtools import debug
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import PlainTextResponse
from PIL import Image
from tensorflow import make_tensor_proto
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

from src.dependencies import get_random_image, get_settings, httpx_client
from src.factories import make_triton_grpc_client
from src.inference import AVAILABLE_SERVINGS
from src.torchserve_grpc_inference_client import inference_pb2, inference_pb2_grpc
from src.types import Servings

logger: Final = logging.getLogger(__name__)
router: Final = APIRouter()

try:
    from tritonclient.grpc import InferInput, InferRequestedOutput
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


@router.post(
    "/infer/{serving_type}",
    response_class=PlainTextResponse,
    summary="Performs GRPC inference for an image",
)
async def _(
    *,
    serving_type: Servings,
    client: httpx.AsyncClient = Depends(httpx_client),
    image: UploadFile = File(...),
) -> str:
    """
    Performs inference for the input image (JPEG).
    Based on the value of `serving_type`, it selects the correct
    backend implementation for the model and calls this backend.

    The output of the model is discarded.
    """
    image_content = io.BytesIO(cast(bytes, await image.read()))
    inference_function, service_url = AVAILABLE_SERVINGS[serving_type]

    await inference_function(client=client, image_content=image_content, url=service_url)

    return "OK"


@router.get(
    "/randinfer/{serving_type}",
    response_class=PlainTextResponse,
    summary="Performs GRPC inference for an image",
)
async def _(*, serving_type: Servings, random_image: Path = Depends(get_random_image)) -> str:
    """
    Performs inference for the input image (JPEG).
    Based on the value of `serving_type`, it selects the correct
    backend implementation for the model and calls this backend.

    The output of the model is discarded.
    """

    async with aiofiles.open(random_image, mode="rb") as f:
        image_content = io.BytesIO(await f.read())

    # TODO This is ugly
    if serving_type == Servings.torchserve:
        await torchserve_grpc(image_content)
    elif serving_type == Servings.tfserving:
        await tfserving_grpc(image_content)
    elif serving_type == Servings.triton_pytorch:
        await triton_pytorch_grpc(image_content)
    elif serving_type == Servings.triton_tensorflow:
        await triton_tensorflow_grpc(image_content)

    return "OK"


async def triton_pytorch_grpc(image_content: BinaryIO) -> None:
    triton_client = make_triton_grpc_client()

    jpeg_rgb = Image.open(image_content).convert("RGB")
    jpeg_rgb = jpeg_rgb.resize((224, 224))
    normalized_jpeg = (np.array(jpeg_rgb) - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
    normalized_jpeg = np.expand_dims(np.einsum("ijk->kij", np.array(normalized_jpeg)), 0).astype(np.float32)

    infer_input = InferInput("input__0", [1, 3, 224, 224], "FP32")
    infer_input.set_data_from_numpy(normalized_jpeg)
    output = InferRequestedOutput("output__0")
    response = triton_client.infer("resnet-50-torch", model_version="1", inputs=[infer_input], outputs=[output])

    assert response.as_numpy("output__0").tolist()


async def triton_tensorflow_grpc(image_content: BinaryIO) -> None:
    triton_client = make_triton_grpc_client()

    jpeg_rgb = Image.open(image_content).convert("RGB")
    jpeg_rgb = jpeg_rgb.resize((224, 224))
    jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).astype(np.float32)

    infer_input = InferInput("input_1", [1, 224, 224, 3], "FP32")
    infer_input.set_data_from_numpy(jpeg_rgb)
    output = InferRequestedOutput("activation_49")
    response = triton_client.infer("resnet-50-tensorflow", model_version="1", inputs=[infer_input], outputs=[output])

    assert response.as_numpy("activation_49").tolist()


async def tfserving_grpc(image_content: BinaryIO) -> None:
    async with grpc.aio.insecure_channel(get_settings().tfserving_grpc_host) as channel:
        stub_tf = prediction_service_pb2_grpc.PredictionServiceStub(channel)

        request = predict_pb2.PredictRequest()
        request.model_spec.name = "resnet_50_classification"
        request.model_spec.signature_name = "serving_default"

        jpeg_rgb = Image.open(image_content).convert("RGB")
        jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0)
        jpeg_rgb = jpeg_rgb.astype(np.float32)

        request.inputs["input_1"].CopyFrom(make_tensor_proto(jpeg_rgb))

        response = await stub_tf.Predict(request)
        debug(response)


async def torchserve_grpc(image_content: BinaryIO) -> None:
    async with grpc.aio.insecure_channel(get_settings().torchserve_grpc_host) as channel:
        stub = inference_pb2_grpc.InferenceAPIsServiceStub(channel)
        input_data = {"data": image_content.read()}
        response = await stub.Predictions(inference_pb2.PredictionsRequest(model_name="resnet-50", input=input_data))
        debug(response)
