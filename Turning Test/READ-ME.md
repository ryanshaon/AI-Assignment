# Turing Test + CAPTCHA (Mini Project)

This repo demonstrates:
1) A simple Turing Test style chat where a Judge talks to two participants (Human + AI).
2) A simple CAPTCHA system to protect the "submit verdict" action.

## Features
- Flask server providing endpoints
- In-memory session management (easy to understand)
- AI agent stub (rule-based, replaceable with any LLM later)
- CAPTCHA: random math/text challenge with expiry + attempts
- Logging + evaluation metrics

## How to Run
1. Install dependencies:
   pip install flask

2. Start server:
   python server.py

3. Open in browser:
   http://127.0.0.1:5000

## Files
- server.py        -> main web app + API routes
- ai_agent.py      -> AI participant logic
- human.py         -> human participant interface (demo handler)
- evaluation.py    -> scoring + session results
- logger.py        -> structured logging
- architecture.md  -> design explanation
