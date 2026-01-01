#!/usr/bin/env python3
import os
import datetime
import html as html_lib
import re
import requests

from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SYSTEM_SENDER_EMAIL = os.getenv("SYSTEM_SENDER_EMAIL")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# ===============================
# PASTE YOUR PREMIUM HTML HERE
# ===============================
PREMIUM_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HackRoot — Message Received</title>

<style>
/* ================= RESET ================= */
body{
  margin:0;
  padding:0;
  background:#020617;
  font-family:Inter,Arial,Helvetica,sans-serif;
}
table{border-collapse:collapse}

/* ================= WRAPPER ================= */
.wrapper{
  width:100%;
  padding:44px 14px;
  background:
    radial-gradient(900px 420px at 50% -120px, rgba(124,58,237,0.18), transparent 60%),
    linear-gradient(180deg, #040b22, #020617);
}

/* ================= CARD ================= */
.card{
  max-width:720px;
  margin:auto;
  border-radius:22px;
  overflow:hidden;
  background:linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
  border:1px solid rgba(255,255,255,0.12);
  box-shadow:
    0 40px 140px rgba(2,6,23,0.85),
    inset 0 1px 0 rgba(255,255,255,0.18);
}

/* ================= HEADER ================= */
.header{
  padding:24px 28px;
  display:flex;
  align-items:center;
  gap:16px;
  background:#020617;
  border-bottom:1px solid rgba(255,255,255,0.18);
}

.logo{
  height:48px;
  width:48px;
  padding:10px;              /* was 6px */
  border-radius:14px;

  background:#020617;

  border:1px solid rgba(255,255,255,0.18);

  box-shadow:
    inset 0 0 0 1px rgba(255,255,255,0.12),
    inset 0 0 20px rgba(120,51,254,0.22),
    0 10px 30px rgba(2,6,23,0.9);

  display:flex;
  align-items:center;
  justify-content:center;
}


.brand{
  display:flex;
  flex-direction:column;
  justify-content:center;
  gap:6px;                 /* 👈 clean vertical spacing */
  line-height:1.15;        /* 👈 fixes cramped look */
    padding-top:2px;   /* subtle vertical correction */

}

.brand h1{
  margin:0;
  font-size:1.45rem;
  font-weight:900;
  letter-spacing:.4px;
  color:#ffffff;
}

.year-show{
  display:block;
  margin-top:6px;
  font-size:0.7rem;
  font-weight:700;
  letter-spacing:0.18em;
  text-transform:uppercase;
  color:rgba(207,231,255,0.75);
  white-space:nowrap;   /* keeps it clean */
}




.brand-root{ color:#7833fe; }


/* ================= HERO ================= */
/* ================= HERO ================= */
.hero{
  width:100%;
  max-height:960px;        /* 👈 roughly 1/2 size */
  object-fit:cover;        /* keeps premium crop */
  display:block;
}


/* ================= CONTENT ================= */
.content{
  padding:36px 36px 40px;
  background:linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
  border-top:1px solid rgba(255,255,255,0.08);
}

.content h2{
  margin:0 0 14px;
  font-size:1.6rem;
  font-weight:900;
  color:#ffffff;
}

.content p{
  margin:0 0 20px;
  font-size:1rem;
  line-height:1.75;
  color:#cfe7ff;
}

/* ================= MESSAGE BOX ================= */
.message-box{
  margin-top:24px;
  padding:22px 24px;
  background:linear-gradient(180deg, rgba(124,58,237,0.12), rgba(255,255,255,0.03));
  border-radius:18px;
  border:1px solid rgba(124,58,237,0.35);
  box-shadow:
    0 12px 40px rgba(124,58,237,.25),
    inset 0 1px 0 rgba(255,255,255,.25);
  font-size:.95rem;
  line-height:1.7;
  color:#e6f2ff;
}

.message-box strong{ color:#ffffff; }

/* ================= CTA ================= */
.cta{
  display:inline-block;
  margin-top:30px;
  padding:15px 28px;
  background:linear-gradient(90deg, #22c55e, #4ade80);
  box-shadow:
  0 10px 28px rgba(34,197,94,.45);

  color:#022c22;
  font-weight:900;
  text-decoration:none;
  border-radius:16px;
  font-size:.95rem;
  letter-spacing:.02em;
}

/* ================= FOOTER ================= */
.email-footer{
  padding:28px 20px 30px;
  background:linear-gradient(180deg, rgba(0,0,0,0.45), rgba(0,0,0,0.65));
  text-align:center;
}

.email-divider{
  height:1px;
  margin-bottom:22px;
  background:linear-gradient(
    90deg,
    transparent,
    rgba(124,58,237,.9),
    rgba(34,197,94,.9),
    transparent
  );
}

.email-logo{
  font-size:1.4rem;
  font-weight:900;
  letter-spacing:.4px;
}

.logo-h{ color:#ffffff; }
.logo-r{ color:#7833fe; }

.email-badge{
  display:inline-block;
  margin:10px 0 14px;
  padding:6px 14px;
  font-size:.7rem;
  font-weight:800;
  letter-spacing:.12em;
  border-radius:999px;
  background:linear-gradient(90deg, #22c55e, #4ade80);
  color:#022c22;
}

.email-tagline{
  font-size:.88rem;
  color:rgba(207,231,255,.85);
  margin:0 0 12px;
}

.email-socials{
  margin:16px auto 8px;
}

.email-socials td{
  padding:0 10px;          /* 👈 more breathing room */
}


.email-socials img{
   width:22px;
  height:22px;
  padding:7px;             /* 👈 slightly larger hit area */
  border-radius:10px;
  background:linear-gradient(180deg, rgba(255,255,255,.18), rgba(255,255,255,.05));
  border:1px solid rgba(255,255,255,.35);
}

.email-copy{
  margin-top:14px;
  font-size:.72rem;
  color:rgba(207,231,255,.55);
}

/* ================= MOBILE ================= */
@media(max-width:600px){
  .content{padding:26px 22px 30px}
  .header{padding:20px}
}
</style>
</head>

<body>
<div class="wrapper">
  <div class="card">

    <!-- HEADER -->
    <div class="header">
      <img src="https://res.cloudinary.com/dberju8k2/image/upload/f_auto,q_auto,w_160/Untitled_design_10_f02us1.png" class="logo" alt="HackRoot">
      <div class="brand">
        <h1>hack<span class="brand-root">Root</span></h1>
        <div class="year-show">Request received · __YEAR__</div>
      </div>
    </div>
    <!-- HERO -->
    <img src="https://res.cloudinary.com/dberju8k2/image/upload/f_auto,q_auto,w_1200/hero-email-less-ratio_hfsuxj.webp" class="hero" alt="HackRoot">

    <!-- CONTENT -->
    <div class="content">
      <h2>Hi __NAME__,</h2>
      <p>Thanks for reaching out to <strong>HackRoot</strong>. We’ve received your message and our team is already reviewing it.</p>

      <div class="message-box">
        <strong>Your message</strong><br><br>
        __MESSAGE__
        __PHONE_BLOCK__
        __GITHUB_BLOCK__
      </div>

      <a href="mailto:__RECIPIENT__?subject=Re%3A%20HackRoot" class="cta">
        Reply directly for faster support
      </a>
    </div>

    <!-- FOOTER -->
    <div class="email-footer">
      <div class="email-divider"></div>

      <h3 class="email-logo">
        <span class="logo-h">hack</span><span class="logo-r">Root</span>
      </h3>

      <span class="email-badge">
        🛡 Built for Hackathons • Secure by Design
      </span>

      <p class="email-tagline">
        An elite hackathon team engineering AI-first, production-ready systems.
      </p>

      <table class="email-socials" align="center">
        <tr>
          <td><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn"></td>
          <td><img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" alt="Instagram"></td>
          <td><img src="https://cdn-icons-png.flaticon.com/512/733/733579.png" alt="X"></td>
          <td><img src="https://cdn-icons-png.flaticon.com/512/2111/2111370.png" alt="Discord"></td>
        </tr>
      </table>

      <p class="email-copy">
        © __YEAR__ hackRoot · Built with precision & trust
      </p>
    </div>


  </div>
</div>
</body>
</html>
"""

# ===============================
# RECAPTCHA VERIFY
# ===============================
def verify_recaptcha(token, ip):
    try:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": RECAPTCHA_SECRET_KEY,
                "response": token,
                "remoteip": ip
            },
            timeout=5
        )
        return r.json().get("success", False)
    except Exception:
        return False

# ===============================
# RESEND SEND FUNCTION
# ===============================
def send_email(to, subject, html, reply_to=None):
    payload = {
        "from": SYSTEM_SENDER_EMAIL,
        "to": to,
        "subject": subject,
        "html": html
    }
    if reply_to:
        payload["reply_to"] = reply_to

    r = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=3
    )

    if r.status_code >= 300:
        raise Exception(r.text)

# ===============================
# ROUTES
# ===============================
@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute")
def submit():

    # 🛡 Honeypot
    if request.form.get("company"):
        return {"status": "blocked"}, 200

    # 🔐 CAPTCHA
    captcha_token = request.form.get("g-recaptcha-response")
    if not captcha_token or not verify_recaptcha(captcha_token, request.remote_addr):
        return {"status": "error", "message": "Captcha failed"}, 403

    # 📥 Form data
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    github = request.form.get("github", "").strip()
    message = request.form.get("message", "")

    phone_digits = re.sub(r"\D", "", phone)
    display_phone = f"+91{phone_digits}" if len(phone_digits) == 10 else ""
    year = datetime.datetime.now().year

    # ===============================
    # MESSAGE HANDLING (PAST APP LOGIC)
    # ===============================
    raw_message = message.strip()

    if raw_message:
        safe_message = html_lib.escape(raw_message)
        safe_message = (
            safe_message
            .replace("\r\n", "<br>")
            .replace("\n", "<br>")
            .replace("\r", "<br>")
        )
    else:
        safe_message = (
            "<em style='color:#cfe7ff;'>"
            "No message was written. Our team will contact you based on the details provided."
            "</em>"
        )

    # ===============================
    # USER EMAIL (PREMIUM)
    # ===============================
    user_html = (
        PREMIUM_HTML_TEMPLATE
        .replace("__YEAR__", str(year))
        .replace("__NAME__", html_lib.escape(name))
        .replace("__MESSAGE__", safe_message)
        .replace("__PHONE_BLOCK__", f"<br><b>Phone:</b> {display_phone}" if display_phone else "")
        .replace("__GITHUB_BLOCK__", f"<br><b>Profile:</b> {html_lib.escape(github)}" if github else "")
    )

    # ===============================
    # SUPPORT EMAIL
    # ===============================
    support_html = f"""
    <h3>New HackRoot Enquiry</h3>
    <p><b>Name:</b> {html_lib.escape(name)}</p>
    <p><b>Email:</b> {html_lib.escape(email)}</p>
    <p><b>Phone:</b> {html_lib.escape(display_phone)}</p>
    <p><b>Profile:</b> {html_lib.escape(github)}</p>
    <hr>
    <p><b>Message:</b><br>{safe_message}</p>
    """

    # ===============================
    # SEND EMAILS (FAST RESPONSE)
    # ===============================
    try:
        # 1️⃣ Send user email (wait)
        send_email(
            to=[email],
            subject="Thanks for contacting HackRoot",
            html=user_html
        )
    except Exception as e:
        print("User mail failed:", e)
        return {"status": "error", "message": "Mail failed"}, 500

    # 2️⃣ Respond immediately to frontend
    response = {"status": "success"}

    # 3️⃣ Send support mail (best effort, no delay)
    try:
        send_email(
            to=[SUPPORT_EMAIL],
            subject=f"📩 New Enquiry from {name}",
            html=support_html,
            reply_to=email
        )
    except Exception as e:
        print("Support mail failed:", e)

    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
