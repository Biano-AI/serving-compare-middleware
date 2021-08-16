--instance-market-options MarketType=spot \
)
--env-file test.env


```bash
ssh-keygen -t ed25519
cat .ssh/id_ed25519.pub
# https://github.com/Biano-AI/serving-compare-middleware/settings/keys
```



```bash
git@github.com:Biano-AI/serving-compare-middleware.git
```


--------------

```bash
aws ec2 describe-instances \
        --filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values=Servings-Experiment" \
        --output json
        
aws ec2 describe-instances \
        --filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values=Middleware-Experiment" \
        --query 'Reservations[*].Instances[*].[InstanceId, PrivateIpAddress, PublicIpAddress, PrivateDnsName]' \
        --output json
        
        
aws ec2 describe-instances \
        --filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values=Middleware-Experiment" \
        --query 'Reservations[*].Instances[*].[InstanceId]' \
        --output text
        
        
ssh ubuntu@xxx
ssh ubuntu@xxx

{
    bash <(curl -fsSL https://get.docker.com)
    sudo usermod -aG docker ubuntu
    newgrp docker
}


ssh-keygen -t ed25519
https://docs.docker.com/compose/install/

{
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
}

<!--https://k6.io/docs/getting-started/installation/-->
{
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
    echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
    sudo apt-get update
    sudo apt-get install k6
}
```



```
aws ec2 describe-images \
        --region eu-west-1 \
        --owners amazon \
        --filters "Name=name,Values=Deep Learning AMI (Ubuntu 18.04) Version *" "Name=state,Values=available" \
        --query "reverse(sort_by(Images, &Name))[:1].ImageId" \
        --output text
        
        
aws ec2 describe-images \
        --region eu-west-1 \
        --owners 099720109477 \
        --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*" "Name=state,Values=available" \
        --query "reverse(sort_by(Images, &Name))[:1].ImageId" \
        --output text
```

Mid-July 2021 is the last AMI ID: `ami-081764442f732173f`


ami-03caf24deed650e2c


docker-machine create --driver amazonec2 --amazonec2-region "eu-west-1" --amazonec2-root-size "128" --amazonec2-ami ami-081764442f732173f --amazonec2-instance-type "g4dn.xlarge" --amazonec2-request-spot-instance servings-machine



Prerekvizity


