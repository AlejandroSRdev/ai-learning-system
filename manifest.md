# 📄 AI Learning System — Design Specification

## 1. Overview

This system is a controlled, state-driven learning backend that adapts explanations based on user performance.

It is designed to demonstrate:

- Controlled integration of AI (LLM as non-deterministic dependency)
- Persistent state management
- Deterministic decision-making on top of AI outputs
- Iterative system behavior (not one-shot generation)

## 2. Core Concept

The system operates in three explicit modes:

- Explanation → Generate explanation based on current state
- Evaluation → Generate structured test
- Correction → Evaluate answers, update state, decide next step

Only Correction modifies the system state.

## 3. Tech Stack

### Backend
- FastAPI
- Async support
- Clear API structure
- Easy deployment

### Database
- PostgreSQL
- Relational integrity
- Explicit state modeling
- Strong consistency

### Deployment
- Fly.io
- Simple Docker-based deployment
- Suitable for lightweight production demos

### AI Layer
- LLM (OpenAI / similar)
  - Used for:
    - Explanation generation
    - Evaluation generation
    - Answer correction
- Always constrained via prompts and validated outputs

## 4. System Architecture

```
Client (UI / API consumer)
        ↓
FastAPI (Application Layer)
        ↓
Domain Logic (Decision System)
        ↓
Database (PostgreSQL)
        ↓
LLM (External Dependency)
```

## 5. Data Model

### 5.1 Table: students

Stores static and semi-static information about the student.

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    level VARCHAR(50),
    goal TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.2 Table: learning_state

Represents the current state of the learning process.

```sql
CREATE TABLE learning_state (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    current_topic TEXT,
    last_score FLOAT,
    iteration INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_student
        FOREIGN KEY(student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);
```

**Notes:**
- This is the source of truth for system decisions
- last_score drives adaptation
- iteration tracks progression cycles

### 5.3 Table: evaluations

Stores each evaluation attempt.

```sql
CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    topic TEXT,
    questions JSONB,
    answers JSONB,
    score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_student_eval
        FOREIGN KEY(student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);
```

### 5.4 Relationships
- students (1) → (N) learning_state
- students (1) → (N) evaluations

However, in practice:

- One active learning_state per student
- Multiple evaluations over time

## 6. System Flow

### 6.1 Explanation Mode

Endpoint:
`POST /explain/{student_id}`

Flow:

- Fetch student + learning_state
- Determine difficulty from last_score
- Generate explanation via LLM
- Return structured explanation

Important:

- Does NOT modify state

### 6.2 Evaluation Mode

Endpoint:
`POST /evaluate/{student_id}`

Flow:

- Fetch student + current_topic
- Generate 10-question test via LLM
- Return structured questions

Important:

- Does NOT modify state

### 6.3 Correction Mode (Core of System)

Endpoint:
`POST /correct/{student_id}`

Input:

- User answers

Flow:

- Evaluate answers (LLM or logic)
- Compute score (0–1)
- Store evaluation
- Update learning_state:
  - last_score
  - iteration + 1
- Apply decision logic:

```python
def decide_next_step(score):
    if score < 0.5:
        return "simplify"
    elif score < 0.75:
        return "reinforce"
    else:
        return "advance"
```

Return:

```json
{
  "score": 0.6,
  "decision": "reinforce"
}
```

## 7. Decision Layer (Key Differentiator)

The system is not driven by the LLM, but by deterministic logic.

**Control Rules:**
- LLM generates content
- Backend decides:
  - difficulty
  - progression
  - repetition

## 8. AI Integration Strategy

**Principles:**
- AI is non-trusted
- All outputs must be:
  - structured
  - validated
- No direct persistence without validation

**Example Evaluation Output Schema**

```json
{
  "score": 0.7,
  "mistakes": [
    "incorrect chain rule application"
  ]
}
```

## 9. API Endpoints Summary

- `POST /students`
- `POST /explain/{student_id}`
- `POST /evaluate/{student_id}`
- `POST /correct/{student_id}`
- `GET  /students/{student_id}/state`

## 10. Deployment

### Fly.io Setup
- Dockerized FastAPI app
- Environment variables:
  - DATABASE_URL
  - OPENAI_API_KEY

**Steps:**
- Build Docker image
- Deploy via Fly CLI
- Connect to managed PostgreSQL

## 11. Key Design Decisions

### 1. Explicit Modes over AI Inference
- Ensures deterministic flow
- Reduces ambiguity

### 2. State-Driven System
- Behavior depends on persisted data
- Enables reproducibility

### 3. Separation of Concerns
- AI generates
- Backend decides
- DB persists

### 4. Minimal Scope
- Only one topic at a time
- Only one learning cycle loop
- No multi-agent complexity

## 12. What This System Demonstrates

- Ability to design AI systems under control
- Understanding of stateful workflows
- Proper handling of non-deterministic dependencies
- Translation of a real-world problem into a structured backend system

## 13. Next Step

This document defines the system boundary and structure.

Next phase:

→ Implement endpoints
→ Define prompts + validation
→ Run full cycle end-to-end
