# ML Pipeline - Digital Medical Report Organizer

This directory contains the machine learning pipeline for processing medical reports using OCR and AI technologies.

## Overview

The ML pipeline consists of several components:
- **OCR Processing**: Extract text from medical report images
- **AI Analysis**: Use medical language models for entity extraction and analysis
- **Data Processing**: Clean and structure extracted medical data
- **Model Management**: Handle model loading and inference

## Directory Structure

```
ml_pipeline/
├── ocr/              # OCR processing scripts
├── ai/               # AI model inference
├── models/           # Model storage and management
├── utils/            # Utility functions
├── data/             # Sample data and test files
└── requirements.txt  # Python dependencies
```

## Features

### OCR Processing
- Multi-language text extraction
- Image preprocessing for better accuracy
- Support for various medical document formats
- Quality assessment and validation

### AI Analysis
- Medical Named Entity Recognition (NER)
- Document classification
- Risk assessment
- Clinical data extraction
- Automated insights generation

### Models Used
- **Emergent Medical NER**: For medical entity extraction
- **Medical Classification**: For document type classification
- **Custom Models**: Fine-tuned for specific medical domains

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download required models:
```bash
python -m ml_pipeline.models.download_models
```

3. Run OCR processing:
```bash
python -m ml_pipeline.ocr.process_image --input path/to/image.jpg
```

4. Run AI analysis:
```bash
python -m ml_pipeline.ai.analyze_text --text "extracted text"
```

## API Integration

The ML pipeline integrates with the FastAPI backend through:
- RESTful endpoints for processing requests
- Async processing for large files
- Real-time status updates
- Error handling and logging

## Performance

- **OCR Speed**: ~2-5 seconds per page
- **AI Analysis**: ~1-3 seconds per document
- **Memory Usage**: ~2-4GB for full pipeline
- **GPU Support**: CUDA acceleration available

## Configuration

Set environment variables in `.env`:
```env
MODEL_CACHE_DIR=./models
OCR_LANGUAGE=eng
AI_MODEL_NAME=emergentmedical/emergent-medical-ner
MAX_FILE_SIZE=10485760
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Include comprehensive docstrings
4. Write unit tests for new features
5. Update documentation for changes
