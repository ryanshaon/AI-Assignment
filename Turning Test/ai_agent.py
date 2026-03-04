import random

BOT_STYLES = [
    "slightly_formal",
    "friendly",
    "short_answers",
]

def generate_reply(history, user_msg: str) -> str:
    """
    Simple AI stub. Replace this function with a real model call later.
    history: list of (role, msg)
    """
    style = random.choice(BOT_STYLES)

    if "your name" in user_msg.lower():
        return "I’d rather not say. 🙂"

    if style == "slightly_formal":
        return f"I understand. Based on what you said: {summarize(user_msg)}"
    if style == "short_answers":
        return random.choice(["Yeah.", "Not sure.", "Maybe.", "Could be."])
    return f"Haha okay 😄 Tell me more about: {pick_topic(user_msg)}"

def summarize(text: str) -> str:
    text = text.strip()
    if len(text) <= 40:
        return text
    return text[:40] + "..."

def pick_topic(text: str) -> str:
    words = [w.strip(".,!?").lower() for w in text.split() if len(w) > 3]
    if not words:
        return "that"
    return random.choice(words)
