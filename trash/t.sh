XX=$(
  aws ec2 describe-images \
    --region eu-west-1 \
    --owners amazon \
    --filters "Name=name,Values=Deep Learning AMI (Ubuntu 18.04) Version *" "Name=state,Values=available" \
    --query "reverse(sort_by(Images, &Name))[:1].ImageId" \
    --output text
)



