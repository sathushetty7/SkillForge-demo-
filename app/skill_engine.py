"""Deterministic, explainable skill normalization and gap analysis.

This first version intentionally avoids claiming proficiency from a resume alone.
Skills found in the profile are marked as declared; proficiency needs assessment
or project evidence before the planner can treat it as verified.
"""

ALIASES = {
    "js": "javascript",
    "javascript": "javascript",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "py": "python",
    "python": "python",
    "powerbi": "power bi",
    "power bi": "power bi",
    "ms excel": "excel",
    "microsoft excel": "excel",
}

LEVELS = {"beginner": 1, "intermediate": 2, "advanced": 3}


def normalize_skill(skill: str) -> str:
    cleaned = " ".join(skill.lower().strip().split())
    return ALIASES.get(cleaned, cleaned)


def analyze_gaps(student: dict, job: dict) -> dict:
    student_skills = {normalize_skill(s) for s in student.get("skills", []) if s.strip()}
    projects = student.get("projects", [])
    rows = []
    total_weight = 0
    weighted_gap = 0

    for requirement in job["requirements"]:
        skill = requirement["skill"]
        canonical = normalize_skill(skill)
        importance = requirement.get("importance", "required")
        weight = 2 if importance == "required" else 1
        total_weight += weight

        if canonical in student_skills:
            status = "declared_unverified"
            gap = 0.5
            explanation = (
                "This skill appears in the student profile, but proficiency should be "
                "verified with an assessment or project evidence."
            )
        else:
            status = "not_found_in_profile"
            gap = 1.0
            explanation = (
                "This skill was not found in the supplied profile; confirm with the "
                "student before treating it as a confirmed skill gap."
            )

        weighted_gap += weight * gap
        rows.append({
            "skill": skill,
            "normalized_skill": canonical,
            "importance": importance,
            "required_level": requirement.get("required_level", "intermediate"),
            "status": status,
            "gap_estimate": round(gap, 2),
            "explanation": explanation,
        })

    gap_score = round((weighted_gap / total_weight) * 100) if total_weight else 0
    return {
        "student_name": student.get("name", "Student"),
        "job_title": job["title"],
        "weekly_hours": student.get("weekly_hours", 10),
        "skill_results": rows,
        "estimated_gap_score": gap_score,
        "score_note": (
            "Heuristic estimate based on profile presence and requirement importance; "
            "not a validated measure of employability. Listed skills are unverified "
            "until supported by assessments or project evidence."
        ),
        "next_step": "Use these results to prioritize assessments and build a 12-week plan.",
        "project_count_in_profile": len(projects),
    }
