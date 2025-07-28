# main.py - FastAPI server
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
from ai_math_generator import AIEnhancedMathGenerator

app = FastAPI(title="Math Practice API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global generator instance (in production, you'd use a database)
generator = AIEnhancedMathGenerator()

# Pydantic models for request/response
class GenerateProblemsRequest(BaseModel):
    operations: List[str]
    count: int

class RecordAttemptRequest(BaseModel):
    problem: Dict
    user_answer: int
    time_taken: float

class Problem(BaseModel):
    problem: str
    answer: int
    operation: str
    difficulty: int
    ai_adapted: bool = False

@app.get("/")
async def root():
    return {"message": "Math Practice API is running!"}

@app.post("/generate-problems", response_model=List[Problem])
async def generate_problems(request: GenerateProblemsRequest):
    """Generate adaptive math problems"""
    try:
        problems = generator.generate_adaptive_problems(
            request.operations, 
            request.count
        )
        return problems
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/record-attempt")
async def record_attempt(request: RecordAttemptRequest):
    """Record student's attempt for AI learning"""
    try:
        generator.record_student_attempt(
            request.problem,
            request.user_answer,
            request.time_taken
        )
        return {"status": "success", "message": "Attempt recorded"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/student-insights")
async def get_student_insights():
    """Get AI insights about student performance"""
    try:
        insights = generator.get_student_insights()
        return insights
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset-session")
async def reset_session():
    """Reset the current session (clear performance data)"""
    global generator
    generator = AIEnhancedMathGenerator()
    return {"status": "success", "message": "Session reset"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)