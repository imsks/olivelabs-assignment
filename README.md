# NLQ Full-Stack Application

A production-ready Natural Language Query (NLQ) application that converts business questions into SQL queries with explainability and data visualization.

## 🚀 Features

-   **Natural Language to SQL**: Convert business questions into safe SQL queries using OpenAI GPT-4
-   **Query Explainability**: Understand how queries are built with structured explanations
-   **Data Visualization**: Automatic chart inference and rendering (bar, line, pie charts)
-   **Conversational Context**: Follow-up queries that maintain conversation history
-   **SQL Safety**: Comprehensive validation against dangerous operations
-   **Real-time Results**: Fast query execution with caching
-   **Modern UI**: Responsive design with dark mode support

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

-   Docker and Docker Compose
-   Node.js 18+ (for local development)
-   Python 3.11+ (for local development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd olivelabs-assignment
```

### 2. Environment Configuration

```bash
cp env.example .env
# Edit .env with your OpenAI API key and other settings
```

### 3. Start with Docker

```bash
docker-compose up -d
```

This will start:

-   PostgreSQL database on port 5432
-   Redis on port 6379
-   Backend API on port 8000
-   Frontend on port 3000

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed sample data
docker-compose exec backend python -c "from app.core.seed_data import generate_sample_data; generate_sample_data()"
```

### 5. Access the Application

-   Frontend: http://localhost:3000
-   API Docs: http://localhost:8000/docs
-   Health Check: http://localhost:8000/health

## 📊 Sample Queries

Try these natural language queries:

-   "Show me revenue by region"
-   "What are the top 10 customers by revenue?"
-   "Orders in Q2 2024"
-   "Break down revenue by product line"
-   "Average order value by customer segment"

## 🔧 Development

### Backend Development

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📚 API Documentation

### Core Endpoints

-   `POST /api/nlq/query` - Main NLQ endpoint (parse + execute)
-   `POST /api/nlq/parse` - Parse NLQ to SQL only
-   `POST /api/nlq/execute` - Execute SQL query
-   `POST /api/conversation/refine` - Handle follow-up queries
-   `GET /api/schema/describe` - Get database schema

### Authentication

-   `POST /api/auth/login` - User login
-   `POST /api/auth/register` - User registration

## 🧪 Testing

### Acceptance Criteria

-   ✅ NLQ produces correct SQL for filter + group + aggregate + order + limit
-   ✅ Follow-up queries modify previous context correctly
-   ✅ SQL safety rejects dangerous operations
-   ✅ Explain object accurately mirrors produced SQL
-   ✅ Chart inference works for groupable numeric outputs

### Test Coverage

-   Unit tests for all service modules
-   Integration tests for API endpoints
-   Component tests for React components
-   Golden test prompts for NLQ parsing

## 🔒 Security Features

-   JWT-based authentication
-   SQL injection prevention
-   Query whitelist validation
-   Rate limiting and timeouts
-   CORS configuration
-   Input sanitization

## 📈 Performance

-   Redis caching for query results
-   Connection pooling for database
-   Lazy loading for large datasets
-   Optimized SQL generation
-   Frontend code splitting

## 🚀 Deployment

### Production Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

See `env.example` for all required configuration options.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues:

1. Check the API documentation at `/docs`
2. Review the test cases for examples
3. Open an issue on GitHub

---

Built with ❤️ for the Olivelabs assignment
