from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Literal

from app.skill_engine import analyze_gaps
from app.resume_parser import extract_text_from_pdf

app = FastAPI(
    title="SkillForge AI API",
    description="Core skill-to-job analysis engine for the Skills-to-Job Planner.",
    version="0.1.0",
)

class StudentProfile(BaseModel):
    name: str = "Student"
    education: str | None = None
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    weekly_hours: int = Field(default=10, ge=1, le=80)

class JobRequirement(BaseModel):
    skill: str
    importance: Literal["required", "preferred"] = "required"
    required_level: Literal["beginner", "intermediate", "advanced"] = "intermediate"

class JobDescription(BaseModel):
    title: str
    requirements: list[JobRequirement]

class GapAnalysisRequest(BaseModel):
    student: StudentProfile
    job: JobDescription

@app.get("/health")
def health():
    return {"status": "ok", "service": "skillforge-ai"}

@app.post("/api/skills/gaps")
def skill_gaps(request: GapAnalysisRequest):
    if not request.job.requirements:
        raise HTTPException(status_code=422, detail="Provide at least one job skill requirement.")
    return analyze_gaps(request.student.model_dump(), request.job.model_dump())

@app.post("/api/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    file_bytes = await file.read()

    try:
        text = extract_text_from_pdf(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read this PDF. Please upload a valid PDF."
        )

    return {
        "filename": file.filename,
        "extracted_text": text
    }