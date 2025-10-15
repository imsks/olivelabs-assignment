#!/bin/bash

# Simple setup script for NLQ Full-Stack App
echo "🚀 Setting up NLQ Full-Stack Application..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Check if Node.js 18+ is installed
node_version=$(node --version 2>&1 | cut -d'v' -f2 | cut -d'.' -f1)
required_node_version="18"

if [ "$node_version" -lt "$required_node_version" ]; then
    echo "❌ Node.js 18+ is required. Current version: $(node --version)"
    exit 1
fi

echo "✅ Python and Node.js versions are compatible"

# Create virtual environment for backend
echo "📦 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Setup frontend
echo "📦 Setting up frontend dependencies..."
cd ../frontend
npm install
echo "✅ Frontend dependencies installed"

# Copy environment file
echo "⚙️ Setting up environment..."
cd ..
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Created .env file from template"
    echo "⚠️  Please edit .env file with your OpenAI API key and other settings"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Start the application: docker-compose up -d"
echo "3. Initialize database: docker-compose exec backend alembic upgrade head"
echo "4. Seed data: docker-compose exec backend python -c \"from app.core.seed_data import generate_sample_data; generate_sample_data()\""
echo "5. Access the app: http://localhost:3000"
echo ""
echo "For local development:"
echo "- Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "- Frontend: cd frontend && npm run dev"
