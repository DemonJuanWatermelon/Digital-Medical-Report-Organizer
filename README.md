# Digital Medical Report Organizer

A comprehensive AI-powered system for managing, processing, and analyzing medical reports with advanced OCR capabilities and intelligent data extraction.

## 🏥 Overview

The Digital Medical Report Organizer is a modern web application that transforms how medical professionals handle and analyze patient reports. By combining cutting-edge OCR technology with advanced AI models, it automatically extracts, categorizes, and analyzes medical information from scanned documents, providing valuable insights and improving workflow efficiency.

The system processes medical images through a sophisticated pipeline that includes image preprocessing, text extraction, medical entity recognition, document classification, and risk assessment. Healthcare providers can upload reports, view AI-generated analysis, and access organized patient data through an intuitive web interface.

## 🚀 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend**: Next.js, React, Tailwind CSS, TypeScript
- **ML/AI**: Transformers, PyTorch, Tesseract OCR, Emergent Medical LLM
- **Database**: PostgreSQL with full-text search
- **Infrastructure**: Docker, Docker Compose, Kubernetes, Nginx
- **Authentication**: JWT-based security with role-based access control

## ✨ Key Features

- **📄 OCR Processing**: Advanced image preprocessing and text extraction from medical documents
- **🤖 AI Analysis**: Medical entity recognition, document classification, and risk assessment
- **🔍 Smart Search**: Full-text search across all processed reports
- **📊 Analytics Dashboard**: Comprehensive insights and statistics
- **🔒 Secure Storage**: Encrypted data storage with access controls
- **📱 Responsive Design**: Modern UI that works on all devices
- **⚡ Real-time Processing**: Live status updates and progress tracking

## 🏗️ Project Structure

```
/
├─ backend/           # FastAPI backend application
│   ├─ app/          # Main application code
│   ├─ requirements.txt
│   └─ Dockerfile
├─ frontend/         # Next.js frontend application
│   ├─ app/          # Next.js app directory
│   ├─ components/   # React components
│   ├─ package.json
│   └─ tailwind.config.js
├─ ml_pipeline/      # OCR and AI processing
│   ├─ ocr/          # OCR processing scripts
│   ├─ ai/           # AI model inference
│   └─ requirements.txt
├─ infra/            # Infrastructure and deployment
│   ├─ docker-compose.yml
│   ├─ nginx.conf
│   └─ k8s/          # Kubernetes manifests
├─ docs/             # Comprehensive documentation
│   ├─ api/          # API documentation
│   ├─ architecture/ # System architecture
│   └─ deployment/   # Deployment guides
└─ README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 13+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Digital-Medical-Report-Organizer
   ```

2. **Set up environment variables**:
   ```bash
   cd infra
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

For detailed local development setup, see the [Local Development Guide](docs/deployment/local-development.md).

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### ML Pipeline Setup

```bash
cd ml_pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[System Architecture](docs/architecture/system-overview.md)**: Detailed system design and components
- **[API Reference](docs/api/rest-api.md)**: Complete REST API documentation
- **[Deployment Guide](docs/deployment/)**: Docker, Kubernetes, and production deployment
- **[User Guide](docs/user-guide/)**: End-user documentation and tutorials

## 🔧 Configuration

### Environment Variables

Key environment variables for configuration:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/medical_reports

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract
OCR_LANGUAGE=eng

# AI Models
AI_MODEL_NAME=emergentmedical/emergent-medical-ner
```

## 🧪 Testing

### Run Tests

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test

# ML pipeline tests
cd ml_pipeline
pytest tests/
```

### Test Coverage

```bash
# Backend coverage
cd backend
pytest --cov=app tests/

# Frontend coverage
cd frontend
npm run test:coverage
```

## 🚀 Deployment

### Docker Deployment

```bash
cd infra
docker-compose -f docker-compose.yml up -d
```

### Kubernetes Deployment

```bash
kubectl apply -f infra/k8s/
```

### Production Deployment

See the [Production Deployment Guide](docs/deployment/production.md) for detailed instructions.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Next.js](https://nextjs.org/) for the React framework
- [Transformers](https://huggingface.co/transformers/) for AI model integration
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
- [Emergent Medical](https://emergentmedical.ai/) for medical AI models

## 📊 Project Status

- ✅ **Backend API**: Complete with authentication and file processing
- ✅ **Frontend UI**: Modern React interface with dark/green theme
- ✅ **ML Pipeline**: OCR and AI processing with medical models
- ✅ **Infrastructure**: Docker and Kubernetes deployment ready
- ✅ **Documentation**: Comprehensive guides and API docs
- 🔄 **Testing**: Unit and integration tests in progress
- 🔄 **CI/CD**: Automated testing and deployment pipeline

---

**Built with ❤️ for the healthcare community**
