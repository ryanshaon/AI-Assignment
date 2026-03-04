# Architecture

## Modules

### 1) server.py (API + Session Manager)
Responsibilities:
- Create and manage sessions ("rooms")
- Assign roles: judge, participantA, participantB
- Route messages between judge and participants
- Call AI agent when it's AI’s turn
- Enforce CAPTCHA verification on final verdict submission

### 2) ai_agent.py (AI Participant)
Responsibilities:
- Generate replies using simple heuristics (demo)
- Pluggable: can be swapped for an LLM later

### 3) human.py (Human Participant)
Responsibilities:
- Represents the human participant behavior for demo purposes
- In real use: this would be a second UI/client connected live

### 4) evaluation.py (Evaluation)
Responsibilities:
- Collect transcript + verdict
- Compute metrics:
  - judge_correct (0/1)
  - num_messages
  - duration_seconds

### 5) logger.py (Logging)
Responsibilities:
- Save logs to console and a file (optional extension)
- Keep timestamps for each message

## High-Level Flow

1. Judge opens homepage -> creates session
2. Server creates:
   - Participant A (human)
   - Participant B (AI)
   (hidden assignment)
3. Judge chats with A and B (separately)
4. Judge requests CAPTCHA
5. Judge submits verdict + CAPTCHA answer
6. Server verifies CAPTCHA -> stores evaluation result
