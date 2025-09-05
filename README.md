# CI/CD Pipeline with FastAPI

A production-ready FastAPI application with PostgreSQL database integration, Docker containerization, and automated CI/CD pipeline for EC2 deployment.

## 🚀 Features

- **FastAPI Framework**: High-performance async API framework
- **PostgreSQL Integration**: Robust database with connection pooling
- **Docker Support**: Multi-stage containerized deployment
- **CI/CD Pipeline**: Automated testing, building, and EC2 deployment
- **Database Connectivity**: Fixed Docker networking with host mode
- **Health Monitoring**: Robust health checks with retry logic
- **API Documentation**: Interactive Swagger UI and ReDoc
- **Testing Infrastructure**: Unit, integration, and E2E tests
- **Environment Debugging**: Comprehensive logging and variable display

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- Git

## 🛠️ Installation

### Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd fastapi-boilerplate
   ```

2. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up PostgreSQL database**

   ```bash
   # Create database
   createdb app_db

   # Run initialization script
   psql app_db < init.sql
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

### Docker Development

1. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/v1/health

## 🧪 Testing

### Run all tests

```bash
pytest
```

### Run specific test types

```bash
# Unit tests
pytest tests/ -m unit

# E2E tests
pytest tests/e2e/ -m e2e

# Integration tests
pytest tests/ -m integration
```

### Run with coverage

```bash
pytest --cov=app --cov-report=html
```

## 🐳 Docker

### Build Docker image

```bash
docker build -t fastapi-boilerplate .
```

### Run Docker container

```bash
docker run -p 8000:8000 \
  -e DB_HOST=localhost \
  -e DB_PORT=5432 \
  -e DB_NAME=app_db \
  -e DB_USER=app_user \
  -e DB_PASSWORD=your_password \
  fastapi-boilerplate
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Configuration

### Environment Variables

| Variable      | Description       | Default     |
| ------------- | ----------------- | ----------- |
| `DB_HOST`     | Database host     | `localhost` |
| `DB_PORT`     | Database port     | `5432`      |
| `DB_NAME`     | Database name     | `app_db`    |
| `DB_USER`     | Database user     | `app_user`  |
| `DB_PASSWORD` | Database password | -           |
| `DB_MIN_CONN` | Min connections   | `1`         |
| `DB_MAX_CONN` | Max connections   | `20`        |
| `HOST`        | Server host       | `0.0.0.0`   |
| `PORT`        | Server port       | `8000`      |
| `LOG_LEVEL`   | Logging level     | `INFO`      |

## 📚 API Documentation

### Endpoints

- `GET /` - Root endpoint with API information
- `GET /api/v1/health` - Health check endpoint
- `GET /api/v1/status` - API status endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Example Usage

```bash
# Health check
curl "http://localhost:8000/api/v1/health"

# API status
curl "http://localhost:8000/api/v1/status"
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

1. **CI Pipeline** (`.github/workflows/ci.yml`)

   - Code linting and formatting with Black
   - Unit and E2E testing with pytest
   - PostgreSQL database testing
   - Coverage reporting
   - Test result artifacts

2. **CD Pipeline** (`.github/workflows/cd.yml`)

   - Automated deployment to EC2
   - Docker image building and pushing to Docker Hub
   - SSH deployment with environment variables
   - Health check verification
   - Old image cleanup

### Workflow Triggers

- **Push to main/develop**: Runs CI pipeline
- **Pull Request**: Runs CI pipeline
- **CI success**: Automatically triggers CD pipeline
- **Manual trigger**: Can be run manually from GitHub Actions

## 🚀 Automatic Deployment

### **How to Deploy**

1. **Go to GitHub Actions**

   - Navigate to your repository on GitHub
   - Click on "Actions" tab
   - Find "CD Pipeline" workflow

2. **Click "Run workflow"**

   - Optionally enter a version tag (e.g., `v1.0.0`)
   - Click "Run workflow"

3. **Monitor deployment**
   - Watch the workflow run in real-time
   - Check logs for any issues
   - Verify deployment success

### **Deployment Process**

1. **Builds Docker image** with your code
2. **Pushes to Docker Hub** (regsim/ci-cd-pipeline)
3. **SSH to EC2** and runs deployment script
4. **Pulls latest image** from Docker Hub
5. **Stops old container** and starts new one
6. **Runs health check** with retry logic
7. **Cleans up old images**

### **EC2 Server Setup**

The CD pipeline automatically deploys to your EC2 instance. You need to:

1. **Set up GitHub Secrets** (see [EC2_SETUP.md](EC2_SETUP.md))
2. **Install Docker on EC2**
3. **Configure PostgreSQL database**
4. **Set up SSH access**

**Quick Setup:**

```bash
# Install Docker on EC2
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo usermod -aG docker ec2-user

# Install PostgreSQL
sudo yum install -y postgresql postgresql-server
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Test deployment
curl http://your-ec2-ip:8000/api/v1/health
```

**Full setup guide:** See [EC2_SETUP.md](EC2_SETUP.md) for detailed instructions.

### **Deployment Features**

- **Host Networking**: Uses `--network host` for database connectivity
- **Environment Variables**: Secure credential management
- **Health Check Retry**: Up to 6 attempts with 10-second intervals
- **Database Setup**: Automatic PostgreSQL configuration
- **Image Cleanup**: Removes old Docker images to save space
- **Debug Logging**: Comprehensive environment variable display

## 🏗️ Project Structure

```
ci-cd-pipeline/
├── app/                    # Application code
│   ├── config/            # Database configuration
│   ├── database/          # Connection pooling
│   ├── models/            # Pydantic models
│   ├── routes/            # API routes
│   └── services/          # Business logic
├── tests/                 # Test suite
│   ├── e2e/              # End-to-end tests
│   ├── fixtures/         # Test data
│   └── utils/            # Test utilities
├── .github/workflows/     # GitHub Actions CI/CD
├── docker-compose.yml     # Local development
├── Dockerfile            # Multi-stage container
├── deploy.sh             # EC2 deployment script
├── requirements.txt      # Python dependencies
├── init.sql              # Database initialization
└── main.py              # Application entry point
```

## 🌐 External Access

### **Accessing Your API from Outside EC2**

1. **Configure Security Group**

   ```bash
   # Allow inbound traffic on port 8000
   aws ec2 authorize-security-group-ingress \
     --group-id sg-xxxxxxxxx \
     --protocol tcp \
     --port 8000 \
     --cidr 0.0.0.0/0
   ```

2. **Get Your EC2 Public IP**

   ```bash
   curl http://169.254.169.254/latest/meta-data/public-ipv4
   ```

3. **Test External Access**

   ```bash
   # Health check
   curl http://YOUR-EC2-PUBLIC-IP:8000/api/v1/health

   # API documentation
   http://YOUR-EC2-PUBLIC-IP:8000/docs
   ```

### **Troubleshooting**

- **Container shows "unhealthy"**: Check if `curl` is installed in Docker image
- **Database connection fails**: Verify PostgreSQL is running and configured
- **Health check times out**: Check security group allows port 8000
- **Deployment fails**: Check GitHub Secrets are properly configured

## 🔒 Security

- **Input validation** with Pydantic
- **SQL injection protection** with parameterized queries
- **Environment variable security** with GitHub Secrets
- **Docker security** with non-root user
- **Network security** with host networking
- **Private key protection** with .gitignore

## 📊 Monitoring

- **Health checks** for all services
- **Structured logging** with configurable levels
- **Database connection monitoring**
- **Performance metrics** (via FastAPI)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test cases for usage examples
