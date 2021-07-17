# FastAPI middleware for comparing different ML model serving approaches

## About this project

This server, written in [FastAPI](https://fastapi.tiangolo.com/), serves as middleware between the client and selected ML model serving tools ([Tensorflow Serving](https://github.com/tensorflow/serving), [TorchServe](https://github.com/pytorch/serve) and [NVIDIA Triton](https://github.com/triton-inference-server/server)).

It allows the client to infer using a unified and very simple JSON API.

This project has been created to support a paper to test the performance of selected serving tools. Therefore, the outputs from the models are gathered but not further parsed and returned to the client (in other words, the client just sends JPEGs and receives no results, only 200 HTTP responses).

The resulting JSON API is really not complicated at all. All you need is a curl like this:

```bash
$ curl -vS http://localhost:8000/infer/${SERVING_TYPE} \
        -F "image=@path/to/local/image.JPG"
```

Where `SERVING_TYPE` can be one of:

* `torchserve`
* `tfserving`
* `triton_pytorch`
* `triton_tensorflow`

## For developers

* If you want to develop this project, the instructions are here: [docs/DEVELOPMENT](./docs/DEVELOPMENT.md)
* If you want to perform a performance test, the instructions are here: [docs/AWS_SETUP](./docs/AWS_SETUP.md)

## About our team

TBD

## Contact us

TBD


## License

The MIT License (MIT) <br>
Copyright (c) 2021 Biano AI <[ai-research@biano.com](mailto:ai-research@biano.com)>
