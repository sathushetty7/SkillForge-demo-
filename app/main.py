from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Literal

from app.skill_engine import analyze_gaps
from app.resume_parser import extract_text_from_pdf
from app.skill_extractor import extract_skills
from app.job_roles import JOB_ROLES
from app.roadmap_engine import generate_roadmap

app = FastAPI(
    title="SkillForge AI API",
    description="AI-powered skill gap analysis and career planning API.",
    version="0.1.0",
)


# -----------------------------
# Request Models
# -----------------------------

class StudentProfile(BaseModel):
    name: str = "Student"
    education: str | None = None
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    weekly_hours: int = Field(default=10, ge=1, le=80)


class JobRequirement(BaseModel):
    skill: str
    importance: Literal["required", "preferred"] = "required"
    required_level: Literal[
        "beginner", "intermediate", "advanced"
    ] = "intermediate"


class JobDescription(BaseModel):
    title: str
    requirements: list[JobRequirement]


class GapAnalysisRequest(BaseModel):
    student: StudentProfile
    job: JobDescription


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health", tags=["default"])
def health():
    return {
        "status": "ok",
        "service": "skillforge-ai",
    }


# -----------------------------
# Skill Gap Analysis
# -----------------------------

@app.post("/api/skills/gaps", tags=["Skills"])
def skill_gaps(request: GapAnalysisRequest):
    if not request.job.requirements:
        raise HTTPException(
            status_code=422,
            detail="Provide at least one job skill requirement.",
        )

    return analyze_gaps(
        request.student.model_dump(),
        request.job.model_dump(),
    )


# -----------------------------
# Resume Parsing
# -----------------------------

@app.post("/api/resume/parse", tags=["Resume"])
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume.",
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume.",
        )

    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty.",
            )

        text = extract_text_from_pdf(file_bytes)
        detected_skills = extract_skills(text)

        return {
            "filename": file.filename,
            "extracted_text": text,
            "detected_skills": detected_skills,
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Unable to read this PDF. Please upload a valid PDF.",
        ) from exc


# -----------------------------
# Job Role Selection
# -----------------------------

@app.get("/api/job-roles", tags=["Job Roles"])
def list_job_roles():
    return {
        "job_roles": [
            {
                "title": title,
                "required_skills": skills,
            }
            for title, skills in JOB_ROLES.items()
        ]
    }


@app.get("/api/job-roles/{role}", tags=["Job Roles"])
def get_job_role(role: str):
    normalized_role = role.replace("-", " ").strip().lower()

    matching_role = next(
        (
            title
            for title in JOB_ROLES
            if title.lower() == normalized_role
        ),
        None,
    )

    if matching_role is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Job role not found. "
                "Check GET /api/job-roles for available roles."
            ),
        )

    return {
        "title": matching_role,
        "required_skills": JOB_ROLES[matching_role],
    }

# -----------------------------
# Personalized Learning Roadmap
# -----------------------------

class RoadmapRequest(BaseModel):
    target_role: str
    current_skills: list[str] = Field(default_factory=list)
    weekly_hours: int = Field(default=10, ge=1, le=80)


@app.post("/api/roadmap/generate", tags=["Learning Roadmap"])
def create_learning_roadmap(request: RoadmapRequest):
    try:
        return generate_roadmap(
            target_role=request.target_role,
            current_skills=request.current_skills,
            weekly_hours=request.weekly_hours,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
