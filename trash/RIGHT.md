```bash
cat << EOF > haha.env
TFSERVING_SERVICE_URL=http://ip-172-31-40-131.eu-west-1.compute.internal:8501/v1/models/resnet_50_classification:predict
TORCHSERVE_SERVICE_URL=http://ec2-54-171-72-213.eu-west-1.compute.amazonaws.com:8080/predictions/resnet-50
TRITON_SERVICE_HOST=ec2-54-171-72-213.eu-west-1.compute.amazonaws.com:8000
EOF

docker-compose --file docker-compose.middleware.yml --env-file .env up --build --detach web


k6 run --vus 10 --duration 20s         -e MIDDLEWARE_HOST=localhost:8000         -e SERVING_TYPE=triton_pytorch         script.js
```
