from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import logging
import os
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Student Success Intelligence Platform API",
    description="API for student risk prediction and messaging",
    version="1.0.0"
)

# Security: Restrict CORS to specific origins instead of "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],  # Only allow frontend dev server
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow necessary methods
    allow_headers=["Content-Type", "Authorization"],  # Restrict headers
    max_age=3600,  # Cache preflight requests
)

# Request/Response Models with Validation
class StudentInfo(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Student name")
    attendance: float = Field(..., ge=0.0, le=1.0, description="Attendance rate (0.0 to 1.0)")
    scores: List[float] = Field(..., min_length=1, max_length=50, description="List of student scores")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        # Sanitize name to prevent injection
        if not re.match(r'^[a-zA-Z\s\-\.]+$', v):
            raise ValueError('Name contains invalid characters')
        # Prevent XSS by limiting special characters
        sanitized = re.sub(r'[<>"\']', '', v)
        if len(sanitized) != len(v):
            raise ValueError('Name contains potentially dangerous characters')
        return sanitized.strip()
    
    @field_validator('scores')
    @classmethod
    def validate_scores(cls, v):
        # Validate each score is in valid range
        for score in v:
            if not (0 <= score <= 100):
                raise ValueError('Scores must be between 0 and 100')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Alex Johnson",
                "attendance": 0.75,
                "scores": [85, 90, 78, 82]
            }
        }


class RiskPredictionResponse(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score between 0 and 1")


class MessageRequest(BaseModel):
    student_name: str = Field(..., min_length=1, max_length=100, description="Student name")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score between 0 and 1")
    
    @field_validator('student_name')
    @classmethod
    def validate_student_name(cls, v):
        # Sanitize name to prevent injection
        if not re.match(r'^[a-zA-Z\s\-\.]+$', v):
            raise ValueError('Student name contains invalid characters')
        sanitized = re.sub(r'[<>"\']', '', v)
        if len(sanitized) != len(v):
            raise ValueError('Student name contains potentially dangerous characters')
        return sanitized.strip()

    class Config:
        schema_extra = {
            "example": {
                "student_name": "Alex",
                "risk_score": 0.85
            }
        }


class MessageResponse(BaseModel):
    message: str = Field(..., description="Personalized message for student")


# Global Exception Handler
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    logger.warning(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Validation error", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )


@app.get("/")
def read_root():
    return {
        "message": "Student Success Intelligence Platform API",
        "version": "1.0.0",
        "endpoints": ["/health", "/predict-risk", "/message", "/docs"]
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "student-success-api"}


@app.post("/predict-risk", response_model=RiskPredictionResponse, status_code=status.HTTP_200_OK)
async def predict_risk(student_info: StudentInfo):
    """
    Predicts risk score for a student based on their information.
    Currently returns a mock risk score of 0.85.
    """
    try:
        # Log the request for monitoring
        logger.info(f"Risk prediction requested for student: {student_info.name}")
        
        # Mock risk calculation (replace with actual ML model in production)
        # For now, return hardcoded value as specified
        risk_score = 0.85
        
        # Validate the calculated risk score
        if not (0.0 <= risk_score <= 1.0):
            raise ValueError("Calculated risk score is out of valid range")
        
        return RiskPredictionResponse(risk_score=risk_score)
    
    except ValueError as e:
        logger.error(f"Validation error in predict_risk: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in predict_risk: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to predict risk score"
        )


@app.post("/message", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def message(request_data: MessageRequest):
    """
    Generates a personalized message for a student based on their risk score.
    """
    try:
        # Log the request for monitoring
        logger.info(f"Message requested for student: {request_data.student_name}, risk: {request_data.risk_score}")
        
        # Sanitize student name to prevent XSS
        student_name = request_data.student_name
        
        # Generate personalized message based on risk score
        if request_data.risk_score >= 0.7:
            message_text = f"Hi {student_name}, we noticed you missed 2 assignments. Need help?"
        elif request_data.risk_score >= 0.5:
            message_text = f"Hi {student_name}, you're doing well! Keep up the good work."
        else:
            message_text = f"Hi {student_name}, great job staying on track!"
        
        # Additional sanitization of the message
        # Remove any potential script tags or dangerous content
        message_text = re.sub(r'<script[^>]*>.*?</script>', '', message_text, flags=re.IGNORECASE | re.DOTALL)
        
        return MessageResponse(message=message_text)
    
    except ValueError as e:
        logger.error(f"Validation error in message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate message"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
