# AI Platform Interview

Lightweight monorepo that contains a React frontend, an Express backend, and a few Python utility services for resume parsing and face recognition.

This README explains what each part does and how to install and run the project locally.

## Contents / About

- `backend/` — Express API (user management, MongoDB persistence).
- `pythonModules/` — Python microservices and utilities:
  - `main.py` — FastAPI service for profile picture upload / face recognition (used by the frontend).
  - `DocumentParser.py`, `FaceRecognition.py` — helper modules for parsing resumes and face recognition.
- `documentParser/` and `documentParserJS/` — separate parser implementations (Python FastAPI and Node/Express) used in other parts of the workspace.

---

## Prerequisites

- Node.js 18+ and npm (or pnpm)
- Python 3.10+ and pip (for the Python modules)
- MongoDB instance (local or hosted) for the backend
- Optional: `venv` for python virtual environments

Environment variables (examples are below) must be provided for backend and python services.

---

## Installation

Clone the repository and cd into the root `aiInterviewer_backend` folder:

```bash
git clone <your-repo-url>
cd aiInterviewer_backend
```

### Backend (Express)

1. Change into the backend folder and install dependencies:

```bash
cd backend
npm install
```

2. Create a `.env` file (example values):

```ini
PORT=3000
MONGODB_URI=mongodb://localhost:27017
# other env vars as needed
```

### Python modules

1. Create a virtual environment and install dependencies:

```bash
cd ../pythonModules
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.sample.env` to `.env` and update keys (if present). The python modules may expect environment variables (e.g., API keys) depending on which sub-module you run.

---

## Execution guide

Start each service in its own terminal. Below are the common commands used in development.

### Backend

From `aiPlatformInterview/backend`:

```bash
# start backend
npm start
# (or use nodemon if you add it) for dev auto-reload
```

The backend runs by default on port 3000 and needs `MONGODB_URI` set in the `.env` file.

API endpoints (summary):
- GET `/` — health/status
- POST `/users` — create a user
  - body: { name, email, phoneNumber, role, performanceDetails }
- PUT `/users/:id/performance` — update performance for a user

Example curl to create a user:

```bash
curl -X POST http://localhost:3000/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Jane","email":"jane@example.com","phoneNumber":"1234567890","role":"RN","performanceDetails": []}'
```

### Frontend

From `aiPlatformInterview/frontend`:

```bash
npm run dev
```

Vite serves the frontend on `http://localhost:5173` by default.

### Python profile/face service

From `aiPlatformInterview/pythonModules` (virtualenv activated):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Endpoints available in this service include:
- POST `/upload-profile-picture` — multipart form upload of profile picture
- POST `/upload-live-cam-photo` — upload livecam photo
- POST `/face-recognition` — compare profile and livecam photos

These endpoints are used by the frontend components that handle profile pictures and webcam capture.



## Environment variables / .env examples

Backend (`backend/.env`):

```ini
PORT=3000
MONGODB_URI=mongodb://localhost:27017
```

Python profile service (`pythonModules/.env` or system env):

```ini
# optional service-specific settings
# e.g. for any LLM/GROQ keys used by DocumentParser
GROQ_API_KEY=your_groq_key_here
```

Frontend (`frontend/.env`):

```ini
# Place any client-side runtime keys (be careful not to expose secret keys)
VITE_API_BASE_URL=http://localhost:3000
```

---

## Notes & Tips

- CORS: the backend and python services configure CORS for common dev origins. For production, restrict allowed origins.
- Database: ensure `MONGODB_URI` points to a reachable MongoDB instance. For local dev you can run `mongod` or use a hosted MongoDB Atlas cluster.
- The repo contains several parser implementations (Python and JS). Pick the one you intend to deploy and wire the frontend to that service.
- When deploying a single service from this monorepo (e.g., to Render), set the service root to the folder you're deploying (`backend`, `frontend`, or `documentParser`).

