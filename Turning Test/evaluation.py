import time

def evaluate_session(session):
    """
    session dict contains:
      - created_at
      - transcriptA, transcriptB
      - verdict (A/B)
      - ai_side ('A' or 'B')
    """
    duration = int(time.time() - session["created_at"])
    num_msgs = len(session["transcriptA"]) + len(session["transcriptB"])
    judge_correct = 1 if session.get("verdict") == session.get("ai_side") else 0

    return {
        "duration_seconds": duration,
        "num_messages": num_msgs,
        "judge_correct": judge_correct,
        "ai_side": session.get("ai_side"),
        "verdict": session.get("verdict"),
    }
