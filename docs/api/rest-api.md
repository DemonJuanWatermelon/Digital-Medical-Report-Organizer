# REST API Reference

## Base URL
```
http://localhost:8000/api
```

## Authentication

All API endpoints (except public ones) require authentication using JWT tokens.

### Headers
```http
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Reports

#### Upload Medical Report
```http
POST /reports/upload
```

**Request:** Multipart form data
- `file`: Medical report image file (JPG, PNG, etc.)

**Response:**
```json
{
  "id": 1,
  "title": "medical_report.jpg",
  "user_id": 1,
  "file_path": "/uploads/unique_filename.jpg",
  "file_type": "image/jpeg",
  "ocr_text": "Extracted text from the image...",
  "extracted_data": {
    "document_type": "lab_result",
    "confidence": 0.95,
    "entities": {
      "medications": [],
      "conditions": ["diabetes"],
      "procedures": [],
      "measurements": ["120/80 mmHg"]
    }
  },
  "ai_analysis": {
    "summary": "Lab results show normal blood pressure...",
    "key_findings": ["Normal blood pressure reading"],
    "risk_level": "low",
    "follow_up_required": false
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get User Reports
```http
GET /reports?skip=0&limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "medical_report.jpg",
    "created_at": "2024-01-01T00:00:00Z",
    "status": "processed",
    "risk_level": "low"
  }
]
```

#### Get Specific Report
```http
GET /reports/{report_id}
```

**Response:**
```json
{
  "id": 1,
  "title": "medical_report.jpg",
  "user_id": 1,
  "file_path": "/uploads/unique_filename.jpg",
  "file_type": "image/jpeg",
  "ocr_text": "Extracted text...",
  "extracted_data": { ... },
  "ai_analysis": { ... },
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Users

#### Get Current User
```http
GET /users/me
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Get All Users (Admin)
```http
GET /users?skip=0&limit=100
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid file type. Only image files are allowed."
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Report not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- **General API**: 10 requests per second per IP
- **File Upload**: 2 requests per second per IP
- **Authentication**: 5 requests per minute per IP

## File Upload Limits

- **Maximum file size**: 10MB
- **Allowed formats**: JPG, JPEG, PNG, GIF, BMP, TIFF
- **Processing timeout**: 5 minutes

## Response Codes

| Code | Description |
|------|-------------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

## Pagination

List endpoints support pagination using query parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

## Filtering and Sorting

### Reports
- `status`: Filter by processing status (`processing`, `completed`, `error`)
- `risk_level`: Filter by risk level (`low`, `medium`, `high`)
- `created_after`: Filter reports created after this date
- `created_before`: Filter reports created before this date
- `sort_by`: Sort field (`created_at`, `title`, `risk_level`)
- `sort_order`: Sort direction (`asc`, `desc`)

### Example
```http
GET /reports?status=completed&risk_level=high&sort_by=created_at&sort_order=desc&limit=50
```
