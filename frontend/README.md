# SkillForge Frontend

A Next.js dashboard for the SkillForge FastAPI career-roadmap API.

## Requirements
- Node.js 20.9+ (LTS recommended)
- Python backend running on `http://127.0.0.1:8000`

## Run locally
From this directory:

```powershell
Copy-Item .env.local.example .env.local
npm install
npm run dev
```

Open http://localhost:3000.

In another terminal, start the FastAPI backend using your existing project instructions. The Next.js route handler proxies requests to FastAPI, so browser-side CORS configuration is not required for local development.

## Backend URL
Set `BACKEND_API_URL` in `.env.local` to the reachable FastAPI URL. For production, deploy the API separately and set this environment variable in your frontend hosting settings.

## Features
- Fetches job roles from `GET /api/job-roles`
- Uploads PDF resumes to `POST /api/resume/parse`
- Generates a learning plan with `POST /api/roadmap/generate`
- Requests skill-gap analysis from `POST /api/skills/gaps`
- Lets students edit extracted skills and weekly study hours

The dashboard gracefully falls back to common role options when the API is offline. API-backed actions require the backend endpoints to be running.
