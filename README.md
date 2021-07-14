# FastAPI middleware for comparing different ML model serving approaches

## Models

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

Supported Python version is `3.9`.

1. Create and activate [virtual environment](https://docs.python.org/3/library/venv.html)
2. Install `pip install nvidia-pyindex` to install the NVIDIA Triton client from the NVIDIA Private Python Package Index 
3. Install Python dependencies: `pip install -r requirements.txt`
4. Start the application server: `uvicorn api:main --workers=2 --reload`

This project can also be developed and executed using [Docker Compose](https://docs.docker.com/compose/).

To run all the necessary containers, simply run: 

```bash
docker-compose up --build
```

Then open [http://127.0.0.1:8000/docs]() .

:point_right: **Important note:** Docker Compose will start all three servlets at once. This can be very resource intensive on your computer.


## License

The MIT License (MIT) <br>
Copyright (c) 2021 Biano AI <[ai-research@biano.com](mailto:ai-research@biano.com)>
