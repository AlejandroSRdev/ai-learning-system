# AI Learning System

Backend system that models learning as a **state-driven process**, where explanations adapt based on user performance.

The focus is not on generating content, but on **controlling how and when AI is used** within a predictable system.

---

## What it does

- Generates explanations based on user state  
- Evaluates understanding with structured tests  
- Updates performance and adapts next steps  

Core loop:

State → Explanation → Evaluation → Correction → Updated State

---

## Key idea

AI does not control the system.  
The backend does.

- Decisions (progression, difficulty) are deterministic  
- State is persisted (PostgreSQL)  
- AI is used as a constrained generation tool  

---

## Stack

- FastAPI (Python 3.12)  
- PostgreSQL (Supabase)  
- OpenAI API  
- Docker + Fly.io  

---

## Why this project

To demonstrate how to build **reliable AI systems**:

- stateful  
- controllable  
- explainable  

Not just generate outputs, but **design behavior**.