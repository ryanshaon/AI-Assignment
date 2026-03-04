import time
import uuid
import hashlib
import random

from flask import Flask, request, jsonify, render_template_string

from logger import log
from ai_agent import generate_reply
from human import human_reply_stub
from evaluation import evaluate_session

app = Flask(__name__)

# In-memory stores (demo)
SESSIONS = {}
CAPTCHAS = {}  # captcha_id -> {hash, expires_at, attempts_left}

HOME_HTML = """
<!doctype html>
<html>
<head>
  <title>Turing Test + CAPTCHA</title>
  <style>
    body { font-family: Arial; margin: 20px; }
    .box { border: 1px solid #ddd; padding: 12px; margin-bottom: 12px; border-radius: 8px; }
    input, button { padding: 8px; }
    .row { display: flex; gap: 10px; flex-wrap: wrap; }
    pre { background: #f6f6f6; padding: 10px; border-radius: 8px; }
  </style>
</head>
<body>
  <h2>Turing Test Demo (Judge)</h2>

  <div class="box">
    <button onclick="createSession()">Create Session</button>
    <p>Session ID: <b id="sid">-</b></p>
    <p>Chat with A and B (separately). Try to guess which is AI.</p>
  </div>

  <div class="row">
    <div class="box" style="flex:1; min-width: 300px;">
      <h3>Chat A</h3>
      <input id="msgA" placeholder="Message to A" style="width: 80%;" />
      <button onclick="sendMsg('A')">Send</button>
      <pre id="logA"></pre>
    </div>

    <div class="box" style="flex:1; min-width: 300px;">
      <h3>Chat B</h3>
      <input id="msgB" placeholder="Message to B" style="width: 80%;" />
      <button onclick="sendMsg('B')">Send</button>
      <pre id="logB"></pre>
    </div>
  </div>

  <div class="box">
    <h3>CAPTCHA + Verdict</h3>
    <button onclick="newCaptcha()">Get CAPTCHA</button>
    <p>CAPTCHA ID: <b id="cid">-</b></p>
    <p>Challenge: <b id="challenge">-</b></p>

    <div class="row">
      <select id="verdict">
        <option value="A">A is AI</option>
        <option value="B">B is AI</option>
      </select>
      <input id="captchaAnswer" placeholder="CAPTCHA answer" />
      <button onclick="submitVerdict()">Submit Verdict</button>
    </div>

    <pre id="result"></pre>
  </div>

<script>
let sid = null;
let cid = null;

function createSession() {
  fetch('/session/new', {method:'POST'})
    .then(r => r.json())
    .then(d => {
      sid = d.session_id;
      document.getElementById('sid').innerText = sid;
      document.getElementById('logA').innerText = '';
      document.getElementById('logB').innerText = '';
      document.getElementById('result').innerText = '';
    });
}

function sendMsg(side) {
  if (!sid) return alert("Create a session first");
  const inp = document.getElementById(side === 'A' ? 'msgA' : 'msgB');
  const msg = inp.value.trim();
  if (!msg) return;

  fetch('/session/message', {
    method:'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sid, side: side, message: msg})
  })
  .then(r => r.json())
  .then(d => {
    const logEl = document.getElementById(side === 'A' ? 'logA' : 'logB');
    logEl.innerText += "Judge: " + msg + "\\n";
    logEl.innerText += side + ": " + d.reply + "\\n\\n";
    inp.value = '';
  });
}

function newCaptcha() {
  fetch('/captcha/new')
    .then(r => r.json())
    .then(d => {
      cid = d.captcha_id;
      document.getElementById('cid').innerText = cid;
      document.getElementById('challenge').innerText = d.challenge;
    });
}

function submitVerdict() {
  if (!sid) return alert("Create a session first");
  if (!cid) return alert("Get a CAPTCHA first");

  const verdict = document.getElementById('verdict').value;
  const ans = document.getElementById('captchaAnswer').value.trim();

  fetch('/session/verdict', {
    method:'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({session_id: sid, verdict: verdict, captcha_id: cid, captcha_answer: ans})
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById('result').innerText = JSON.stringify(d, null, 2);
  });
}
</script>
</body>
</html>
"""

def _hash_answer(ans: str) -> str:
    return hashlib.sha256(ans.strip().lower().encode("utf-8")).hexdigest()

@app.get("/")
def home():
    return render_template_string(HOME_HTML)

@app.post("/session/new")
def new_session():
    session_id = str(uuid.uuid4())[:8]

    # Randomly choose which side is AI (hidden from judge)
    ai_side = random.choice(["A", "B"])

    SESSIONS[session_id] = {
        "created_at": time.time(),
        "ai_side": ai_side,
        "transcriptA": [],
        "transcriptB": [],
        "verdict": None,
        "evaluation": None,
    }

    log("session_new", {"session_id": session_id, "ai_side_hidden": ai_side})
    return jsonify({"session_id": session_id})

@app.post("/session/message")
def send_message():
    data = request.get_json(force=True)
    session_id = data["session_id"]
    side = data["side"]  # 'A' or 'B'
    msg = data["message"]

    if session_id not in SESSIONS:
        return jsonify({"error": "invalid_session"}), 400
    if side not in ["A", "B"]:
        return jsonify({"error": "invalid_side"}), 400

    session = SESSIONS[session_id]
    transcript_key = "transcriptA" if side == "A" else "transcriptB"

    session[transcript_key].append(("judge", msg))
    log("judge_msg", {"session_id": session_id, "side": side, "msg": msg})

    # Decide reply source
    if session["ai_side"] == side:
        reply = generate_reply(session[transcript_key], msg)
    else:
        reply = human_reply_stub(msg)

    session[transcript_key].append((side, reply))
    log("participant_reply", {"session_id": session_id, "side": side, "reply": reply})

    return jsonify({"reply": reply})

@app.get("/captcha/new")
def captcha_new():
    captcha_id = str(uuid.uuid4())[:8]

    # Simple math captcha
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    challenge = f"What is {a} + {b} ?"
    answer = str(a + b)

    CAPTCHAS[captcha_id] = {
        "hash": _hash_answer(answer),
        "expires_at": time.time() + 90,  # 90 seconds
        "attempts_left": 3
    }

    log("captcha_new", {"captcha_id": captcha_id, "challenge": challenge})
    return jsonify({"captcha_id": captcha_id, "challenge": challenge})

def captcha_verify(captcha_id: str, user_answer: str) -> (bool, str):
    c = CAPTCHAS.get(captcha_id)
    if not c:
        return False, "captcha_not_found"
    if time.time() > c["expires_at"]:
        return False, "captcha_expired"
    if c["attempts_left"] <= 0:
        return False, "captcha_locked"

    if _hash_answer(user_answer) == c["hash"]:
        return True, "ok"

    c["attempts_left"] -= 1
    return False, "captcha_wrong"

@app.post("/session/verdict")
def submit_verdict():
    data = request.get_json(force=True)
    session_id = data["session_id"]
    verdict = data["verdict"]  # 'A' or 'B'
    captcha_id = data["captcha_id"]
    captcha_answer = data["captcha_answer"]

    if session_id not in SESSIONS:
        return jsonify({"error": "invalid_session"}), 400
    if verdict not in ["A", "B"]:
        return jsonify({"error": "invalid_verdict"}), 400

    ok, reason = captcha_verify(captcha_id, captcha_answer)
    if not ok:
        log("verdict_blocked", {"session_id": session_id, "reason": reason})
        return jsonify({"error": "captcha_failed", "reason": reason}), 403

    session = SESSIONS[session_id]
    session["verdict"] = verdict
    session["evaluation"] = evaluate_session(session)

    log("verdict_submitted", {"session_id": session_id, "verdict": verdict, "eval": session["evaluation"]})
    return jsonify({
        "message": "verdict_saved",
        "evaluation": session["evaluation"]
    })

if __name__ == "__main__":
    app.run(debug=True)
