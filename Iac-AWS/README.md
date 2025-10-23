# AWS Infrastructure

Terraform setup for deploying to EKS.

## What's Included

- VPC with public/private subnets
- EKS cluster
- Auto-scaling node group
- ECR repository
- NAT gateways
- IAM roles

## Prerequisites

- AWS CLI configured
- Terraform >= 1.0
- kubectl

## Setup

```bash
aws configure

cd Iac-AWS
terraform init
terraform plan
terraform apply

aws eks update-kubeconfig --region us-east-1 --name todo-app-eks
kubectl get nodes
```

## Push to ECR

```bash
ECR_URL=$(terraform output -raw ecr_repository_url)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URL

docker tag tuheen27/gitops:latest $ECR_URL:latest
docker push $ECR_URL:latest
```

Update image in `k8s/deployment.yaml` with the ECR URL.

## Cost

Monthly estimate (us-east-1):
- EKS: $73
- EC2 (2x t3.medium): ~$60
- NAT Gateway: ~$65
- Total: ~$200/month

## Cleanup

```bash
terraform destroy
```

## S3 Backend

For production, add to `main.tf`:

```hcl
backend "s3" {
  bucket = "your-state-bucket"
  key    = "todo-app/terraform.tfstate"
  region = "us-east-1"
}
```

## Troubleshooting

```bash
aws eks describe-cluster --name todo-app-eks --region us-east-1
aws eks describe-nodegroup --cluster-name todo-app-eks --nodegroup-name todo-app-node-group --region us-east-1
```
