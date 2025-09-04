# FastAPI Boilerplate

A production-ready FastAPI boilerplate with PostgreSQL database integration, connection pooling, comprehensive testing infrastructure, and CI/CD pipeline.

## 🚀 Features

- **FastAPI Framework**: High-performance async API framework
- **PostgreSQL Integration**: Robust database with connection pooling
- **Docker Support**: Containerized deployment with Docker Compose
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Security Scanning**: Automated vulnerability scanning
- **API Documentation**: Interactive Swagger UI and ReDoc
- **Health Checks**: Comprehensive health monitoring
- **Rate Limiting**: Built-in request rate limiting
- **Testing Infrastructure**: Unit, integration, and E2E tests

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
   pip install -r requirements-dev.txt
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

   - Code linting and formatting
   - Unit and E2E testing
   - Security scanning
   - Docker image building

2. **CD Pipeline** (`.github/workflows/cd.yml`)

   - Automated deployment to staging
   - Production deployment on tags
   - Docker image publishing

3. **Security Scan** (`.github/workflows/security.yml`)

   - Weekly vulnerability scanning
   - Dependency security checks

4. **Dependency Update** (`.github/workflows/dependency-update.yml`)
   - Weekly dependency updates
   - Automated PR creation

### Workflow Triggers

- **Push to main/develop**: Runs CI pipeline
- **Pull Request**: Runs CI pipeline
- **Tag creation**: Runs CD pipeline for production
- **Manual dispatch**: Allows manual deployment

## 🏗️ Project Structure

```
fastapi-boilerplate/
├── app/                    # Application code
│   ├── config/            # Configuration
│   ├── database/          # Database layer
│   ├── models/            # Pydantic models
│   ├── routes/            # API routes
│   └── services/          # Business logic
├── tests/                 # Test suite
│   ├── e2e/              # End-to-end tests
│   ├── fixtures/         # Test data
│   └── utils/            # Test utilities
├── .github/workflows/     # GitHub Actions
├── docker-compose.yml     # Docker Compose
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
└── main.py              # Application entry point
```

## 🔒 Security

- **Input validation** with Pydantic
- **SQL injection protection** with parameterized queries
- **Rate limiting** with Nginx
- **Security headers** in responses
- **Automated vulnerability scanning**
- **Dependency security checks**

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
