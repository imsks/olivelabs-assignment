# NLQ Full-Stack Application

A production-ready Natural Language Query (NLQ) application that converts business questions into SQL queries with explainability and data visualization.

## 🚀 Features

-   **Natural Language to SQL**: Convert business questions into safe SQL queries using OpenAI GPT-4
-   **Query Explainability**: Understand how queries are built with structured explanations
-   **Data Visualization**: Automatic chart inference and rendering (bar, line, pie charts)
-   **Conversational Context**: Follow-up queries that maintain conversation history
-   **SQL Safety**: Comprehensive validation against dangerous operations
-   **Real-time Results**: Fast query execution with Redis caching
-   **Modern UI**: Responsive design with clean, intuitive interface
-   **Authentication**: JWT-based user authentication
-   **API Documentation**: Auto-generated FastAPI docs

## 🏗️ Architecture

```
olivelabs-assignment/
├── backend/          # FastAPI + Python
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Configuration, database, security
│   │   ├── models/   # SQLAlchemy models
│   │   └── services/ # Business logic
│   └── alembic/      # Database migrations
├── frontend/         # Next.js + TypeScript
│   ├── app/         # App Router pages
│   ├── components/  # React components
│   ├── lib/         # Utilities and API client
│   └── store/       # Zustand state management
└── docker-compose.yml
```

## 🛠️ Tech Stack

### Backend

-   **FastAPI**: Modern Python web framework
-   **SQLAlchemy**: ORM with Alembic migrations
-   **PostgreSQL**: Primary database
-   **Redis**: Session storage and caching
-   **OpenAI GPT-4**: LLM for NLQ parsing
-   **Pydantic**: Data validation and serialization

### Frontend

-   **Next.js 14**: React framework with App Router
-   **TypeScript**: Type-safe development
-   **Tailwind CSS**: Utility-first styling
-   **Zustand**: Lightweight state management
-   **Recharts**: Data visualization library
-   **Axios**: HTTP client with interceptors

## 🚀 Quick Start

### Prerequisites

-   **Python 3.11+** (required for backend)
-   **Node.js 18+** (required for frontend)
-   **Docker & Docker Compose** (optional, for containerized setup)
-   **OpenAI API Key** (required for NLQ functionality)

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd olivelabs-assignment

# Run the automated setup script
chmod +x setup.sh
./setup.sh

# Or use Makefile
make setup
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development (optional)
pip install -r requirements-dev.txt
```

#### 2. Frontend Setup

```bash
cd frontend
npm install
```

#### 3. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your OpenAI API key and other settings
# OPENAI_API_KEY=your_openai_api_key_here
# JWT_SECRET_KEY=your_jwt_secret_key_here
```

### Option 3: Docker Setup (Containerized)

```bash
# Copy environment file
cp env.example .env

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend alembic upgrade head

# Seed sample data
docker-compose exec backend python -c "from app.core.seed_data import generate_sample_data; generate_sample_data()"
```

### 4. Access the Application

-   **Frontend**: http://localhost:3000
-   **API Docs**: http://localhost:8000/docs
-   **Health Check**: http://localhost:8000/health

## 📊 Sample Queries

Try these natural language queries to get started:

### Basic Queries

-   **"Show me revenue by region"** → Groups orders by region and calculates total revenue
-   **"What are the top 10 customers by revenue?"** → Shows highest revenue customers
-   **"Orders in Q2 2024"** → Filters orders for the second quarter of 2024
-   **"Break down revenue by product line"** → Groups revenue by product categories
-   **"Average order value by customer segment"** → Shows AOV for Enterprise vs SMB

### Follow-up Queries (Conversational)

-   **"Show me revenue by region"** → Initial query
-   **"Break it down by product line"** → Refines to show revenue by region AND product line
-   **"Only show Enterprise customers"** → Adds customer segment filter
-   **"What about Q3?"** → Changes time period to Q3 2024

### Advanced Queries

-   **"Revenue trends by month for Software products"** → Time series with product filter
-   **"Customer count by country for orders over $1000"** → Complex filtering and grouping
-   **"Top 5 products by total quantity sold"** → Ranking and aggregation

## 🔧 Development

### Local Development Setup

#### Backend Development

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development

```bash
cd frontend
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting and formatting
cd backend
source venv/bin/activate
ruff check .
black .
mypy .

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

### Using Makefile (Optional)

For convenience, you can use the provided Makefile:

```bash
# Setup everything
make setup

# Development
make dev          # Start both backend and frontend
make dev-backend  # Start only backend
make dev-frontend # Start only frontend

# Testing
make test         # Run all tests
make test-backend # Run only backend tests
make test-frontend # Run only frontend tests

# Linting
make lint         # Lint all code

# Docker
make docker-up    # Start Docker services
make docker-down  # Stop Docker services
make db-migrate   # Run database migrations
make db-seed      # Seed database

# Cleanup
make clean        # Clean up generated files

# Help
make help         # Show all available commands
```

## 📁 Project Structure

```
olivelabs-assignment/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   ├── routes/     # Route handlers
│   │   │   └── dependencies.py
│   │   ├── core/           # Core configuration
│   │   │   ├── config.py   # Settings
│   │   │   ├── database.py # Database connection
│   │   │   ├── security.py # JWT & password hashing
│   │   │   └── exceptions.py
│   │   ├── models/         # SQLAlchemy models
│   │   └── services/       # Business logic
│   │       ├── nlq_parser.py      # Main NLQ orchestrator
│   │       ├── llm_client.py      # OpenAI integration
│   │       ├── schema_registry.py # Schema management
│   │       ├── safety.py          # SQL validation
│   │       ├── query_executor.py  # Query execution
│   │       ├── viz_inference.py   # Chart inference
│   │       ├── explain_builder.py # Query explanations
│   │       └── sessions.py        # Conversation management
│   ├── alembic/            # Database migrations
│   ├── tests/              # Test files
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # Next.js Frontend
│   ├── app/               # App Router pages
│   ├── components/        # React components
│   │   ├── query/         # Query input components
│   │   ├── results/       # Results display components
│   │   └── explainability/ # Explanation components
│   ├── lib/               # Utilities and API client
│   ├── store/             # Zustand state management
│   ├── types/             # TypeScript definitions
│   └── package.json
├── docker-compose.yml     # Multi-container setup
├── env.example           # Environment template
├── setup.sh              # Automated setup script
├── Makefile              # Development commands
└── README.md
```

## 📚 API Documentation

### Core Endpoints

#### NLQ Processing

-   `POST /api/nlq/query` - Main NLQ endpoint (parse + execute)
-   `POST /api/nlq/parse` - Parse NLQ to SQL only
-   `POST /api/nlq/execute` - Execute SQL query

#### Conversation Management

-   `POST /api/conversation/refine` - Handle follow-up queries

#### Schema Information

-   `GET /api/schema/describe` - Get database schema metadata

### Authentication

-   `POST /api/auth/login` - User login
-   `POST /api/auth/register` - User registration

### Example API Usage

```bash
# Parse a natural language query
curl -X POST "http://localhost:8000/api/nlq/query" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Show me revenue by region"}'

# Response
{
  "columns": ["region", "revenue"],
  "rows": [["North America", 125000], ["Europe", 98000]],
  "inferred_chart": "bar",
  "explain": {
    "filters": [],
    "groupBy": ["region"],
    "aggregates": ["sum(revenue)"],
    "sourceTables": ["orders"]
  },
  "sql": "SELECT region, SUM(quantity * unit_price) as revenue FROM orders GROUP BY region"
}
```

## 🧪 Testing

### Acceptance Criteria

-   ✅ **NLQ produces correct SQL** for filter + group + aggregate + order + limit
-   ✅ **Follow-up queries modify previous context** correctly
-   ✅ **SQL safety rejects dangerous operations** (DROP, INSERT, etc.)
-   ✅ **Explain object accurately mirrors** produced SQL
-   ✅ **Chart inference works** for groupable numeric outputs

### Test Coverage

-   **Unit tests** for all service modules (parser, safety, explain_builder, etc.)
-   **Integration tests** for API endpoints
-   **Component tests** for React components
-   **Golden test prompts** for NLQ parsing validation

### Running Tests

```bash
# Run all tests
make test

# Backend tests only
make test-backend

# Frontend tests only
make test-frontend

# With coverage
cd backend && source venv/bin/activate && pytest --cov=app
```

## 🔒 Security Features

-   **JWT-based authentication** with secure token handling
-   **SQL injection prevention** through parameterized queries
-   **Query whitelist validation** against known tables/columns
-   **Dangerous keyword detection** (DROP, DELETE, INSERT, etc.)
-   **Rate limiting and timeouts** for API protection
-   **CORS configuration** for cross-origin security
-   **Input sanitization** and validation
-   **Password hashing** with bcrypt

## 📈 Performance Features

-   **Redis caching** for query results and sessions
-   **Connection pooling** for database efficiency
-   **Lazy loading** for large datasets
-   **Optimized SQL generation** with proper indexing
-   **Frontend code splitting** for faster loading
-   **Query result pagination** for large result sets
-   **LLM response caching** to reduce API costs

## 🚀 Deployment

### Production Docker

```bash
# Start production services
docker-compose up -d

# Initialize database
docker-compose exec backend alembic upgrade head

# Seed sample data
docker-compose exec backend python -c "from app.core.seed_data import generate_sample_data; generate_sample_data()"
```

### Environment Variables

See `env.example` for all required configuration options:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Database
DATABASE_URL=postgresql://nlq_user:nlq_password@localhost:5432/nlq_app
REDIS_URL=redis://localhost:6379

# Optional
DEBUG=False
LOG_LEVEL=INFO
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Issues

```bash
# Database connection issues
docker-compose logs postgres

# Redis connection issues
docker-compose logs redis

# Backend startup issues
docker-compose logs backend
```

#### Frontend Issues

```bash
# Build issues
cd frontend && npm run build

# Dependency issues
cd frontend && rm -rf node_modules && npm install
```

#### OpenAI API Issues

-   Ensure your API key is valid and has sufficient credits
-   Check rate limits and usage quotas
-   Verify the model (`gpt-4`) is available in your account

### Development Tips

1. **Use the Makefile** for common tasks: `make help`
2. **Check logs** with `docker-compose logs -f [service]`
3. **Reset everything** with `make clean && make setup`
4. **Test API** at http://localhost:8000/docs
5. **Monitor Redis** with `redis-cli monitor`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `make test`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions or issues:

1. **Check the API documentation** at http://localhost:8000/docs
2. **Review the test cases** for usage examples
3. **Check the troubleshooting section** above
4. **Open an issue** on GitHub with:
    - Description of the problem
    - Steps to reproduce
    - Expected vs actual behavior
    - Environment details (OS, Python/Node versions)

## 🎯 Roadmap

### Planned Features

-   [ ] **Rule-based parser** for simple queries (cost optimization)
-   [ ] **Query history** with search and filtering
-   [ ] **Export functionality** (CSV, PDF reports)
-   [ ] **Advanced visualizations** (scatter plots, heatmaps)
-   [ ] **Query templates** for common business questions
-   [ ] **Multi-database support** (MySQL, SQLite)
-   [ ] **Real-time collaboration** on queries
-   [ ] **Query performance metrics** and optimization suggestions

---

Built with ❤️ for the Olivelabs assignment

**Tech Stack**: FastAPI + Next.js + PostgreSQL + Redis + OpenAI GPT-4
