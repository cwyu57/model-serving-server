# Model Serving Server

A FastAPI-based server for serving machine learning models with OCR (Optical Character Recognition) capabilities and comprehensive usage tracking. Built with modern Python tools and containerized for easy deployment.

## Key Features

- **OCR Processing**: Advanced optical character recognition using PyTorch and Torchvision (with fake implementation)
- **Usage Tracking**: Built-in analytics and monitoring for model usage
- **PostgreSQL Database**: Robust data persistence with Alembic migrations
- **AWS Integration**: SQS support via LocalStack for local development
- **Modern Stack**: FastAPI, SQLAlchemy 2.0, Python 3.13
- **Developer Tools**: Type-safe with mypy, formatted with ruff, managed with uv

## Prerequisites

Before you begin, ensure you have the following installed on your macOS system:

### Required Tools

1. **Homebrew** - Package manager for macOS
   ```bash
   # Install Homebrew if you don't have it
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Development Tools**
   ```bash
   brew install uv just gum
   ```
   - `uv` - Fast Python package installer and resolver
   - `just` - Command runner for project tasks
   - `gum` - Tool for glamorous shell scripts (used in migrations)

   **Optional: Enable `just` auto-completion for zsh**

   Add the following to your `~/.zshrc`:
   ```bash
   fpath+=($(brew --prefix)/share/zsh/site-functions)
   autoload -Uz compinit
   compinit
   ```
   Then reload your shell: `source ~/.zshrc`

3. **Docker Desktop** - For running PostgreSQL and LocalStack

   Download and install from [docker.com](https://www.docker.com/products/docker-desktop/)

   This includes both Docker and Docker Compose.

4. **Python 3.13** - Managed automatically by `uv`

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd model-serving-server
```

### 2. Install Python Dependencies

```bash
uv sync --extra dev
```

This will create a virtual environment and install all dependencies defined in `pyproject.toml`.

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Environment
ENVIRONMENT=development

# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=model_serving
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
ENABLE_SQL_ECHO=true

# AWS Configuration (LocalStack)
AWS_ENDPOINT_URL=http://localhost:4566
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
```

### 4. Start Infrastructure Services

Start PostgreSQL and LocalStack containers:

```bash
just infra-up
```

This will start both PostgreSQL and LocalStack in the background. Wait a few seconds for the services to be healthy. You can check the logs with:

```bash
just infra-logs
```

### 5. Run Database Migrations

Apply database schema migrations:

```bash
just migrate
```

### 6. Start the Development Server

You can run the application in different ways:

**Option A: Local Development (Recommended for development)**

Run the app locally while connecting to Docker infrastructure:
```bash
just local
```

This runs the Python app on your local machine (with hot reload) while connecting to PostgreSQL and LocalStack running in Docker containers.

**Option B: Full Docker Stack**

Run everything in Docker (app + infrastructure):
```bash
just dev
```

### 7. Verify Installation

Open your browser and navigate to:

- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/healthz

## Common Commands

The project uses `just` as a task runner. Here are the most common commands:

```bash
# Infrastructure Management
just infra-up        # Start infrastructure (PostgreSQL + LocalStack)
just infra-down      # Stop infrastructure
just infra-logs      # View infrastructure logs

# Database Management (individual services)
just pg-up           # Start PostgreSQL only
just pg-down         # Stop PostgreSQL only
just pg-logs         # View PostgreSQL logs only

# Migrations
just migrate         # Apply migrations
just migrate-create  # Create a new migration
just migrate-down    # Rollback last migration
just migrate-status  # Show current migration
just migrate-history # Show migration history
just codegen-models  # Generate SQLAlchemy models from database

# Development
just local           # Run app locally (connects to Docker infrastructure)
just dev             # Run entire app stack in Docker
```

## Development Tools

The project includes several development tools configured in `pyproject.toml`:

- **ruff**: Linting and code formatting
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality
- **sqlacodegen**: Generate models from database schema

To install development dependencies:

```bash
uv sync --group dev
```

## Project Structure

```
model-serving-server/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configurations (database, etc.)
│   ├── entity/       # Business logic (controllers, use cases)
│   ├── repository/   # Data access layer
│   ├── service/      # External services integration
│   ├── use_case/     # Application use cases
│   ├── models.py     # SQLAlchemy models
│   └── main.py       # FastAPI application
├── alembic/          # Database migrations
├── script/           # Utility scripts
├── justfile          # Task definitions
├── pyproject.toml    # Project dependencies
└── docker-compose.yml # Container orchestration
```
