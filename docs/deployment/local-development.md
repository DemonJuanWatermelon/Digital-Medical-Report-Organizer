# Local Development Setup

This guide will help you set up the Digital Medical Report Organizer for local development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 13+
- **Redis** 6+
- **Tesseract OCR** (for ML pipeline)
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Digital-Medical-Report-Organizer
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start the development server
npm run dev
```

### 4. ML Pipeline Setup

```bash
# Navigate to ML pipeline directory (in a new terminal)
cd ml_pipeline

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download required models
python -m spacy download en_core_web_sm

# Start the ML service
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

## Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/medical_reports

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_HOSTS=http://localhost:3000,http://127.0.0.1:3000

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# OCR
TESSERACT_PATH=/usr/bin/tesseract
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### ML Pipeline (.env)

```env
MODEL_CACHE_DIR=./models
OCR_LANGUAGE=eng
AI_MODEL_NAME=emergentmedical/emergent-medical-ner
```

## Database Setup

### PostgreSQL

1. **Install PostgreSQL** (if not already installed)
2. **Create database**:
   ```sql
   CREATE DATABASE medical_reports;
   CREATE USER medical_user WITH PASSWORD 'medical_password';
   GRANT ALL PRIVILEGES ON DATABASE medical_reports TO medical_user;
   ```

3. **Run migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```

### Redis

1. **Install Redis** (if not already installed)
2. **Start Redis server**:
   ```bash
   redis-server
   ```

## Tesseract OCR Setup

### Windows

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Update `TESSERACT_PATH` in backend `.env`

### macOS

```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

## Development Workflow

### 1. Start All Services

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - ML Pipeline
cd ml_pipeline
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload --port 8001
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ML Pipeline**: http://localhost:8001

### 3. Development Tools

#### Backend
- **API Testing**: Use the interactive docs at http://localhost:8000/docs
- **Database Management**: Use pgAdmin or similar tool
- **Logs**: Check terminal output for detailed logs

#### Frontend
- **Hot Reload**: Changes automatically reload the browser
- **Developer Tools**: Use browser dev tools for debugging
- **TypeScript**: Type checking runs automatically

#### ML Pipeline
- **Model Testing**: Test OCR and AI models independently
- **Performance Monitoring**: Monitor processing times and accuracy

## Common Issues

### 1. Port Already in Use

```bash
# Find process using port
lsof -i :8000  # or netstat -ano | findstr :8000 on Windows

# Kill process
kill -9 <PID>  # or taskkill /PID <PID> /F on Windows
```

### 2. Database Connection Issues

- Check PostgreSQL is running
- Verify connection string in `.env`
- Ensure database exists and user has permissions

### 3. OCR Issues

- Verify Tesseract is installed and in PATH
- Check `TESSERACT_PATH` in backend `.env`
- Test with simple images first

### 4. Model Download Issues

- Check internet connection
- Verify model names in configuration
- Clear model cache and re-download

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

### ML Pipeline Tests

```bash
cd ml_pipeline
pytest tests/
```

## Debugging

### Backend Debugging

1. **Enable debug mode** in `.env`:
   ```env
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```

2. **Use debugger**:
   ```python
   import pdb; pdb.set_trace()
   ```

### Frontend Debugging

1. **Use React DevTools** browser extension
2. **Console logging**:
   ```javascript
   console.log('Debug info:', data);
   ```

3. **Network tab** to inspect API calls

### ML Pipeline Debugging

1. **Test individual components**:
   ```python
   from ocr.text_extractor import MedicalTextExtractor
   extractor = MedicalTextExtractor()
   result = extractor.extract_text('test_image.jpg')
   print(result)
   ```

## Performance Optimization

### Backend
- Use connection pooling for database
- Enable Redis caching
- Optimize database queries

### Frontend
- Use React.memo for expensive components
- Implement virtual scrolling for large lists
- Optimize bundle size

### ML Pipeline
- Use GPU acceleration when available
- Implement model caching
- Optimize image preprocessing

## Next Steps

Once you have the local development environment running:

1. **Explore the API** using the interactive docs
2. **Test file uploads** with sample medical images
3. **Review the codebase** structure and architecture
4. **Make your first changes** and see them reflected
5. **Set up your IDE** with appropriate extensions

For more advanced topics, see:
- [Production Deployment](./production.md)
- [Docker Deployment](./docker.md)
- [API Documentation](../api/rest-api.md)
