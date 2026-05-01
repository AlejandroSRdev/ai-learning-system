# AI Learning System — State-Driven Backend with Controlled AI Integration

## Overview

This project is a backend-focused system that models learning as a **state-driven, iterative process**, where explanations are dynamically adapted based on user performance.

Rather than relying on AI to control behavior, the system enforces a clear separation:

- The **backend owns decision-making**
- The **database persists state**
- The **LLM is used as a constrained generation tool**

The goal is to demonstrate how to build **reliable and controllable AI-powered systems**, not just generate content.

---

## Core Concept

The system operates through three explicit modes:

1. **Explanation**  
   Generates an explanation based on the current learning state.

2. **Evaluation**  
   Produces a structured test aligned with the explanation and level.

3. **Correction**  
   Evaluates user answers, computes a score, and updates the system state.

Only the **Correction phase modifies the system**, making it the core of the learning loop.

---

## System Behavior

Each interaction is part of an iterative cycle: