# Data Mapping: medfaster-backend ↔ aiPlatformInterview

This document details the mapping between medfaster-backend (Postgres) and aiPlatformInterview (MongoDB, Frontend/Backend), including every function/component and the data it requires for integration. No DB operations are performed; this is for API/data contract planning.

---

## Backend (aiPlatformInterview/backend)

### aiQuestionGenerator.js
- **Purpose**: Generates interview questions based on job title and user data.
- **Needs from medfaster-backend**:
  - Candidate's job title (`candidate_profiles.job_title`, `jobs.title`)
  - Candidate's profile info (`candidate_profiles.name`, `candidate_profiles.experience`, `candidate_profiles.skills`)
  - Recruiter/job-specific requirements (`jobs.requirements`, `recruiter_profiles`)

### index.js
- **Purpose**: API endpoints for question generation and user creation.
- **Needs from medfaster-backend**:
  - Candidate/user info (`users.name`, `users.email`, `users.phone`, `users.role`)
  - Performance details (to be updated after interview, mapped to `users.id`)
  - Job title (`jobs.title`, `candidate_profiles.job_title`)
  - Profile photo/document path (`documents.profilePicture`)

### models/User.model.js
- **Purpose**: Stores user info and performance.
- **Needs from medfaster-backend**:
  - Candidate/user info (`users.name`, `users.email`, `users.phone`, `users.role`)
  - Performance details (from interview results, mapped to `users.id`)

---

## Frontend (aiPlatformInterview/frontend)

### Form.jsx
- **Purpose**: Collects user info and job selection.
- **Needs from medfaster-backend**:
  - List of job titles (`jobs.title`)
  - Candidate profile fields (`candidate_profiles.name`, `candidate_profiles.email`, `candidate_profiles.phone`)
  - Profile photo/document path (`documents.profilePicture`)

### Validate.jsx
- **Purpose**: Handles face validation.
- **Needs from medfaster-backend**:
  - Candidate's profile photo path (`documents.profilePicture`)
  - Candidate's userId (`users.id`)

### Interview.jsx
- **Purpose**: Runs the interview session.
- **Needs from medfaster-backend**:
  - Candidate's name (`candidate_profiles.name`)
  - userId (`users.id`)
  - Job title (`jobs.title`, `candidate_profiles.job_title`)
  - Profile photo path (`documents.profilePicture`)
  - Personalized config (custom interview settings, from `candidate_profiles`, `jobs`)

### evaluateMetrics.js
- **Purpose**: Evaluates interview transcript.
- **Needs from medfaster-backend**:
  - Candidate's transcript (linked to `users.id`)
  - Optionally, candidate profile for context (`candidate_profiles`)

### md_useVapiInterview.js
- **Purpose**: Manages interview session and performance tracking.
- **Needs from medfaster-backend**:
  - userId (`users.id`)
  - Candidate info (`candidate_profiles.name`, `candidate_profiles.job_title`)
  - Job title (`jobs.title`, `candidate_profiles.job_title`)

### md_useFaceDetection.js / md_useFaceVerification.js
- **Purpose**: Face detection/verification.
- **Needs from medfaster-backend**:
  - Profile photo path (`documents.profilePicture`)
  - userId (for mapping validation to candidate)

### transcriptUtils.js
- **Purpose**: Formats transcripts.
- **Needs from medfaster-backend**:
  - No direct backend data, but transcript may be linked to candidate/userId for evaluation and storage.

---

## Integration Table

| aiPlatformInterview Function/Component | medfaster-backend Table/Field(s) Needed | Notes |
|---------------------------------------|-----------------------------------------|-------|
| aiQuestionGenerator.js                | candidate_profiles.job_title, jobs.title, candidate_profiles.name, candidate_profiles.experience, candidate_profiles.skills | For generating questions |
| index.js (API endpoints)              | users.*, candidate_profiles.*, jobs.*, documents.profilePicture | For user creation, question generation |
| models/User.model.js                  | users.*, candidate_profiles.*, interview results | For storing user info/performance |
| Form.jsx                              | jobs.title, candidate_profiles.*, documents.profilePicture | For collecting user info/job selection |
| Validate.jsx                          | documents.profilePicture, users.id | For face validation |
| Interview.jsx                         | candidate_profiles.*, jobs.title, documents.profilePicture, users.id | For running interview session |
| evaluateMetrics.js                    | interview transcript, users.id, candidate_profiles.* | For evaluating transcript |
| md_useVapiInterview.js                | users.id, candidate_profiles.*, jobs.title | For managing interview session |
| md_useFaceDetection.js / md_useFaceVerification.js | documents.profilePicture, users.id | For face detection/verification |
| transcriptUtils.js                    | users.id (for linking transcript) | For formatting transcript |

---

## Example Data Flow

1. **User fills Form.jsx** → Fetch job titles and candidate info from medfaster-backend.
2. **User uploads profile photo** → Store/retrieve path from medfaster-backend documents.
3. **Validate.jsx** uses profile photo for face validation.
4. **Interview.jsx** uses candidate info, job title, and config for personalized interview.
5. **aiQuestionGenerator.js** generates questions using job title and candidate profile.
6. **Interview transcript** is evaluated by evaluateMetrics.js and mapped to userId.
7. **Performance details** are updated in medfaster-backend for candidate/user.

---

If you need API contract examples or want to expand this mapping, let me know!
