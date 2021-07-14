# FastAPI middleware for comparing different ML model serving approaches

This server, written in [FastAPI](https://fastapi.tiangolo.com/), serves as middleware between the client and selected ML model serving tools ([Tensorflow Serving](https://github.com/tensorflow/serving), [TorchServe](https://github.com/pytorch/serve) and [NVIDIA Triton](https://github.com/triton-inference-server/server)).

It allows the client to infer using a unified and very simple JSON API.

This project has been created to support a paper to test the performance of selected serving tools. Therefore, the outputs from the models are gathered but not further parsed and returned to the client (in other words, the client just sends JPEGs and receives no results, only 200 HTTP responses).


## Models

https://drive.google.com/drive/folders/11tMhfCH3n91noXD5mBLx8fRytEwPsKXm?usp=sharing

### Tensorflow serving

Download https://tfhub.dev/tensorflow/resnet_50/classification/1 and extract it to `./models/tfserving/1/**`.

### Torchserve

Download https://hynek-pub.s3.eu-west-1.amazonaws.com/resnet-50.mar and put it to `./models/torchserve/resnet-50.mar`.

Next, create configuration file `./models/torchserve/config.properties`:

```properties
inference_address=http://0.0.0.0:8080
job_queue_size=100
install_py_dep_per_model=true
```

### Triton

TBD


The final structure of the models folder must look like this:

```
./models/
├───tfserving
│   └───1
│       │   saved_model.pb
│       │
│       └───variables
│               variables.data-00000-of-00001
│               variables.index
│
└───torchserve
        config.properties
        resnet-50.mar
```

## Configuration

Create a file `.env` in the project root:

```dotenv
TFSERVING_SERVICE_URL = "http://***:8501/v1/models/resnet_50_classification:predict"
TORCHSERVE_SERVICE_URL = "http://***:8080/predictions/resnet-50"
TRITON_SERVICE_URL = "http://..."
```

## How to develop

Supported Python version is `3.9` (Standard CPython). Unfortunately the NVIDIA Triton client [does not support](https://github.com/triton-inference-server/client#download-using-python-package-installer-pip) (July 2021) Windows (at least not with `pip install ...`). All other dependencies are independent of the operating system.

### Local development

1. Create and activate [virtual environment](https://docs.python.org/3/library/venv.html)
2. Install `pip install nvidia-pyindex` to install the NVIDIA Triton client from the NVIDIA Private Python Package Index 
3. Install Python dependencies: `pip install -r requirements.txt`
4. Start the application server: `uvicorn api:main --workers=2 --reload`

### Docker Compose

This project can also be developed and executed using [Docker Compose](https://docs.docker.com/compose/).

To run all the necessary containers, simply run: 

```bash
docker-compose up --build
```

Then open [http://127.0.0.1:8000/docs]() .

:point_right: **Important note:** Docker Compose will start all three servings at once. This can be very resource intensive on your computer.

## License

The MIT License (MIT) <br>
Copyright (c) 2021 Biano AI <[ai-research@biano.com](mailto:ai-research@biano.com)>
