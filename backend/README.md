# Student Success Intelligence Platform - Backend API

FastAPI backend for the Student Success Intelligence Platform.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /predict-risk

Predicts risk score for a student based on their information.

**Request Body:**
```json
{
  "name": "Alex Johnson",
  "attendance": 0.75,
  "scores": [85, 90, 78, 82]
}
```

**Response:**
```json
{
  "risk_score": 0.85
}
```

### POST /message

Generates a personalized message for a student based on their risk score.

**Request Body:**
```json
{
  "student_name": "Alex",
  "risk_score": 0.85
}
```

**Response:**
```json
{
  "message": "Hi Alex, we noticed you missed 2 assignments. Need help?"
}
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

