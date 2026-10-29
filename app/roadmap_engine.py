from math import ceil
from app.job_roles import JOB_ROLES


# ============================================================
# SKILL LEARNING PATHS
# ============================================================

SKILL_PATHS = {
    "Python": {
        "hours": 12,
        "prerequisites": [],
        "resources": [
            {
                "title": "Python Official Tutorial",
                "url": "https://docs.python.org/3/tutorial/",
                "type": "documentation",
            },
            {
                "title": "freeCodeCamp Python Courses",
                "url": "https://www.youtube.com/@freecodecamp",
                "type": "video",
            },
        ],
    },
    "SQL": {
        "hours": 10,
        "prerequisites": [],
        "resources": [
            {
                "title": "SQLBolt",
                "url": "https://sqlbolt.com/",
                "type": "interactive",
            },
            {
                "title": "PostgreSQL Tutorial",
                "url": "https://www.postgresql.org/docs/current/tutorial.html",
                "type": "documentation",
            },
        ],
    },
    "Excel": {
        "hours": 6,
        "prerequisites": [],
        "resources": [
            {
                "title": "Microsoft Excel Help",
                "url": "https://support.microsoft.com/excel",
                "type": "documentation",
            },
        ],
    },
    "Statistics": {
        "hours": 10,
        "prerequisites": [],
        "resources": [
            {
                "title": "Khan Academy Statistics",
                "url": "https://www.khanacademy.org/math/statistics-probability",
                "type": "course",
            },
        ],
    },
    "NumPy": {
        "hours": 6,
        "prerequisites": ["Python"],
        "resources": [
            {
                "title": "NumPy Quickstart",
                "url": "https://numpy.org/doc/stable/user/quickstart.html",
                "type": "documentation",
            },
        ],
    },
    "Pandas": {
        "hours": 8,
        "prerequisites": ["Python", "NumPy"],
        "resources": [
            {
                "title": "Pandas Getting Started",
                "url": "https://pandas.pydata.org/docs/getting_started/",
                "type": "documentation",
            },
        ],
    },
    "Data Analysis": {
        "hours": 8,
        "prerequisites": ["Python", "SQL", "Pandas"],
        "resources": [
            {
                "title": "Kaggle Learn",
                "url": "https://www.kaggle.com/learn",
                "type": "course",
            },
            {
                "title": "Pandas Getting Started",
                "url": "https://pandas.pydata.org/docs/getting_started/",
                "type": "documentation",
            },
        ],
    },
    "Data Visualization": {
        "hours": 8,
        "prerequisites": ["Pandas"],
        "resources": [
            {
                "title": "Matplotlib Tutorials",
                "url": "https://matplotlib.org/stable/tutorials/",
                "type": "documentation",
            },
        ],
    },
    "Machine Learning": {
        "hours": 20,
        "prerequisites": ["Python", "Statistics", "Pandas"],
        "resources": [
            {
                "title": "Google Machine Learning Crash Course",
                "url": "https://developers.google.com/machine-learning/crash-course",
                "type": "course",
            },
            {
                "title": "Scikit-learn User Guide",
                "url": "https://scikit-learn.org/stable/user_guide.html",
                "type": "documentation",
            },
        ],
    },
    "Deep Learning": {
        "hours": 25,
        "prerequisites": ["Python", "Machine Learning"],
        "resources": [
            {
                "title": "PyTorch Tutorials",
                "url": "https://pytorch.org/tutorials/",
                "type": "documentation",
            },
        ],
    },
    "JavaScript": {
        "hours": 12,
        "prerequisites": [],
        "resources": [
            {
                "title": "MDN JavaScript Guide",
                "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
                "type": "documentation",
            },
        ],
    },
    "HTML": {
        "hours": 4,
        "prerequisites": [],
        "resources": [
            {
                "title": "MDN HTML Guide",
                "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content",
                "type": "documentation",
            },
        ],
    },
    "CSS": {
        "hours": 6,
        "prerequisites": ["HTML"],
        "resources": [
            {
                "title": "MDN CSS Guide",
                "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics",
                "type": "documentation",
            },
        ],
    },
    "React": {
        "hours": 15,
        "prerequisites": ["JavaScript", "HTML", "CSS"],
        "resources": [
            {
                "title": "React Learn",
                "url": "https://react.dev/learn",
                "type": "documentation",
            },
        ],
    },
    "Git": {
        "hours": 5,
        "prerequisites": [],
        "resources": [
            {
                "title": "Pro Git Book",
                "url": "https://git-scm.com/book/en/v2",
                "type": "documentation",
            },
        ],
    },
    "Docker": {
        "hours": 10,
        "prerequisites": ["Git"],
        "resources": [
            {
                "title": "Docker Get Started",
                "url": "https://docs.docker.com/get-started/",
                "type": "documentation",
            },
        ],
    },
}


# ============================================================
# SKILL NAME NORMALIZATION
# ============================================================

SKILL_ALIASES = {
    "py": "Python",
    "python": "Python",
    "sql": "SQL",
    "structured query language": "SQL",
    "excel": "Excel",
    "microsoft excel": "Excel",
    "statistics": "Statistics",
    "statistical analysis": "Statistics",
    "numpy": "NumPy",
    "np": "NumPy",
    "pandas": "Pandas",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analysis",
    "data visualization": "Data Visualization",
    "data visualisation": "Data Visualization",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "react": "React",
    "reactjs": "React",
    "git": "Git",
    "github": "Git",
    "docker": "Docker",
}


def _normalize(skill: str) -> str:
    """Return a consistent display name for a skill."""
    cleaned = skill.strip().lower()

    if not cleaned:
        return ""

    return SKILL_ALIASES.get(cleaned, cleaned.title())


# ============================================================
# ROLE MATCHING
# ============================================================

def _find_role(target_role: str) -> str | None:
    """Find a job role without depending on capitalization."""
    normalized_target = target_role.replace("-", " ").strip().casefold()

    for role in JOB_ROLES:
        if role.casefold() == normalized_target:
            return role

    return None


# ============================================================
# ROADMAP GENERATION
# ============================================================

def generate_roadmap(
    target_role: str,
    current_skills: list[str],
    weekly_hours: int = 10,
) -> dict:
    """
    Generate a personalized learning roadmap.

    Skills are ordered by prerequisites.
    Current skills are excluded from the learning plan.
    Weekly scheduled hours never exceed weekly_hours.
    """

    if not isinstance(weekly_hours, int) or isinstance(weekly_hours, bool):
        raise ValueError("weekly_hours must be an integer.")

    if weekly_hours < 1 or weekly_hours > 80:
        raise ValueError("weekly_hours must be between 1 and 80.")

    if not target_role or not target_role.strip():
        raise ValueError("Please provide a target job role.")

    if not isinstance(current_skills, list):
        raise ValueError("current_skills must be a list.")

    if any(not isinstance(skill, str) for skill in current_skills):
        raise ValueError("Every current skill must be a string.")

    matching_role = _find_role(target_role)

    if matching_role is None:
        raise ValueError(
            f"Unknown job role: {target_role}. "
            "Check GET /api/job-roles for available roles."
        )

    # Normalize and deduplicate existing skills.
    known_current = {
        _normalize(skill)
        for skill in current_skills
        if skill.strip()
    }

    # Get the target role's required skills.
    role_skills = {
        _normalize(skill)
        for skill in JOB_ROLES[matching_role]
        if skill.strip()
    }

    # Expand prerequisites recursively.
    # Existing skills are treated as already completed.
    needed = set(role_skills)
    pending = list(role_skills)

    while pending:
        skill = pending.pop()
        details = SKILL_PATHS.get(skill, {})

        for prerequisite in details.get("prerequisites", []):
            normalized_prerequisite = _normalize(prerequisite)

            if (
                normalized_prerequisite not in known_current
                and normalized_prerequisite not in needed
            ):
                needed.add(normalized_prerequisite)
                pending.append(normalized_prerequisite)

    # Do not ask the student to learn skills they already know.
    remaining = needed - known_current

    # Topological ordering.
    # A skill is added only after its prerequisites are completed.
    ordered = []
    completed = set(known_current)

    while remaining:
        available = sorted(
            skill
            for skill in remaining
            if all(
                _normalize(prerequisite) in completed
                or _normalize(prerequisite) not in needed
                for prerequisite in SKILL_PATHS.get(
                    skill, {"prerequisites": []}
                )["prerequisites"]
            )
        )

        if not available:
            unresolved = ", ".join(sorted(remaining))
            raise ValueError(
                "Unable to order skill prerequisites. "
                f"Check for a circular dependency involving: {unresolved}"
            )

        # Add one eligible skill at a time to preserve dependency order.
        skill = available[0]
        ordered.append(skill)
        completed.add(skill)
        remaining.remove(skill)

    # --------------------------------------------------------
    # Build a weekly schedule without exceeding study capacity.
    # Skills can span weeks; dependent skills follow prerequisites.
    # --------------------------------------------------------

    roadmap = []
    total_hours = 0
    week_number = 1
    hours_in_week = 0

    for skill in ordered:
        details = SKILL_PATHS.get(
            skill,
            {
                "hours": 8,
                "prerequisites": [],
                "resources": [],
            },
        )

        skill_hours = details["hours"]
        prerequisites = [
            _normalize(prerequisite)
            for prerequisite in details["prerequisites"]
        ]

        # Skills in the roadmap must have their prerequisites completed
        # earlier in the roadmap or listed as existing student skills.
        unmet_prerequisites = [
            prerequisite
            for prerequisite in prerequisites
            if prerequisite not in known_current
            and prerequisite not in ordered[:len(roadmap)]
        ]

        if unmet_prerequisites:
            raise ValueError(
                f"Prerequisites for {skill} are not satisfied: "
                + ", ".join(unmet_prerequisites)
            )

        start_week = week_number
        hours_remaining = skill_hours

        while hours_remaining > 0:
            available_hours = weekly_hours - hours_in_week

            if available_hours == 0:
                week_number += 1
                hours_in_week = 0
                available_hours = weekly_hours

            hours_this_week = min(hours_remaining, available_hours)

            hours_in_week += hours_this_week
            hours_remaining -= hours_this_week

            if hours_remaining > 0:
                week_number += 1
                hours_in_week = 0

        duration_weeks = week_number - start_week + (
            1 if hours_in_week > 0 else 0
        )

        # If a skill finishes exactly at the end of a week,
        # do not count the next week as part of its duration.
        if hours_in_week == 0:
            duration_weeks = week_number - start_week

        roadmap.append(
            {
                "skill": skill,
                "estimated_hours": skill_hours,
                "week": start_week,
                "estimated_duration_weeks": max(1, duration_weeks),
                "prerequisites": prerequisites,
                "resources": details["resources"],
                "status": "not_started",
            }
        )

        total_hours += skill_hours

    # The total duration reflects the actual sequential schedule.
    estimated_total_weeks = (
        week_number if total_hours > 0 else 0
    )

    # Include existing skills with canonical capitalization.
    normalized_current_skills = sorted(known_current)

    return {
        "target_role": matching_role,
        "current_skills": normalized_current_skills,
        "weekly_hours": weekly_hours,
        "total_estimated_hours": total_hours,
        "estimated_total_weeks": estimated_total_weeks,
        "roadmap": roadmap,
        "note": (
            "Estimates are approximate. Skills are ordered by prerequisites. "
            "Weekly study hours will not exceed your selected limit. "
            "Adjust the plan based on your progress."
        ),
    }