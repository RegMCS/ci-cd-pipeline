# EC2 Setup Guide

This guide helps you set up your EC2 instance to automatically pull and deploy from GitHub Container Registry (GHCR).

## 🔧 Prerequisites

- EC2 instance running Ubuntu/Amazon Linux
- Docker installed on EC2
- SSH access to EC2
- GitHub repository with CI/CD pipeline

## 📋 Step 1: Install Docker on EC2

### For Ubuntu/Debian systems:

```bash
# Update system
sudo apt update

# Install Docker
sudo apt install -y docker.io

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

### For Amazon Linux systems:

```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

### For Amazon Linux 2/2023 (using dnf):

```bash
# Update system
sudo dnf update -y

# Install Docker
sudo dnf install -y docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

## 🔐 Step 2: Set up GitHub Secrets

In your GitHub repository, go to **Settings > Secrets and variables > Actions** and add:

### Required Secrets:

- `EC2_HOST` - Your EC2 public IP or domain
- `EC2_USER` - EC2 username (usually `ubuntu` or `ec2-user`)
- `EC2_SSH_KEY` - Your private SSH key for EC2 access
- `DB_HOST` - Database host (e.g., `localhost` or RDS endpoint)
- `DB_PORT` - Database port (usually `5432`)
- `DB_NAME` - Database name
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password
- `DB_MIN_CONN` - Min database connections (e.g., `1`)
- `DB_MAX_CONN` - Max database connections (e.g., `10`)

### How to get SSH Key:

```bash
# On your local machine, if you don't have a key pair:
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# Copy the private key content:
cat ~/.ssh/id_rsa

# Add this content to EC2_SSH_KEY secret
```

## 🚀 Step 3: Test the Setup

1. **Push code to main branch**
2. **Watch GitHub Actions** - CI should run first
3. **If CI passes** - CD should run automatically
4. **Check EC2** - your app should be running on port 8000

## 🔍 Step 4: Verify Deployment

```bash
# SSH into your EC2
ssh -i ~/.ssh/id_rsa ubuntu@your-ec2-ip

# Check if container is running
docker ps

# Check logs
docker logs fastapi-app

# Test the API
curl http://localhost:8000/api/v1/health
```

## 🛠️ Manual Deployment (if needed)

If you need to deploy manually:

```bash
# SSH into EC2
ssh -i ~/.ssh/id_rsa ubuntu@your-ec2-ip

# Run the deployment script
export GITHUB_REPOSITORY="your-username/ci-cd-pipeline"
export GITHUB_TOKEN="your-github-token"
export GITHUB_ACTOR="your-username"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="app_db"
export DB_USER="app_user"
export DB_PASSWORD="app_password"
export DB_MIN_CONN="1"
export DB_MAX_CONN="10"

chmod +x /tmp/deploy.sh
/tmp/deploy.sh
```

## 🔧 Troubleshooting

### Container won't start:

```bash
# Check logs
docker logs fastapi-app

# Check if port is available
sudo netstat -tlnp | grep :8000
```

### Can't pull from GHCR:

```bash
# Login manually
echo "your-github-token" | docker login ghcr.io -u your-username --password-stdin
```

### Health check fails:

```bash
# Test locally
curl http://localhost:8000/api/v1/health

# Check if database is accessible
docker exec -it fastapi-app curl http://localhost:8000/api/v1/health
```

## 📊 Monitoring

### View running containers:

```bash
docker ps
```

### View container logs:

```bash
docker logs fastapi-app -f
```

### Check resource usage:

```bash
docker stats fastapi-app
```

## 🔄 Automatic Updates

Once set up, your app will automatically update when you:

1. Push code to main branch
2. CI tests pass
3. CD deploys to EC2
4. New container starts with latest code

No manual intervention needed! 🎉
