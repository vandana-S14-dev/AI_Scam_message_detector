🕵️ AI Scam Detection Assistant

An Agentic AI + RAG based system that detects scam messages, assigns risk scores, and provides safety advice using multiple AI agents.

🚀 Problem Statement

Online scams (OTP fraud, phishing, fake job offers) are increasing rapidly.
Most users cannot identify whether a message is safe or dangerous.

This project solves that by:

- Detecting scam patterns
- Assigning a risk score (0–100)
- Giving clear reasoning + safety advice

🧠 How It Works (Architecture)

🔁 Step-by-step Flow

1. User Input
   
   - User pastes a suspicious message

2. RAG (Retrieval Augmented Generation)
   
   - System compares input with known scam patterns using FAISS

3. Multi-Agent AI System
   
   - Pattern Agent → Detects scam patterns
   - Risk Agent → Assigns risk score + label
   - Reasoning Agent → Explains why it is scam
   - Advice Agent → Gives safety tips

4. Final Output
   
   - Risk Dashboard (Score + Label)
   - Patterns detected
   - Explanation
   - Safety advice
   - Final Verdict

🤖 Agents Explanation

🔍 Pattern Agent

Identifies:

- Phishing attempts
- Urgency tactics
- Social engineering

🚨 Risk Agent

Returns structured output:

- Risk Score (0–100)
- Label → Low / Medium / High

🧠 Reasoning Agent

Explains:

- Why message is scam
- What tactics are used

🛡️ Advice Agent

Gives:

- Immediate safety actions
- Prevention tips

📊 Features

✅ RAG-based similarity search (FAISS)
✅ Multi-agent architecture
✅ Risk scoring dashboard
✅ Color-coded UI (Green / Orange / Red)
✅ Bullet-point explanations
✅ Final verdict system
✅ Interactive safety check

🎯 Example Input

Urgent! Your bank account will be blocked today. Verify immediately by sharing OTP.

📌 Example Output

- 🔴 Risk Score: 90 (High)
- ⚠️ Patterns:
  - Phishing attempt
  - Urgency tactic
- 🧠 Reasoning:
  - Asking OTP → security risk
- 🛡️ Advice:
  - Do not share OTP
  - Contact bank directly

🖥️ Tech Stack

- Python
- Streamlit
- FAISS
- Sentence Transformers
- Groq API (LLM)

⚙️ Installation & Run

pip install -r requirements.txt
streamlit run app.py

🔐 API Setup

Add your API key in environment variables:

import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

🌐 Deployment

Deployed using Streamlit Cloud

📢 Final Verdict System

- 🔴 High → Scam detected
- 🟠 Medium → Suspicious
- 🟢 Low → Safe

💡 Key Learning

- Built Agentic AI pipeline
- Implemented RAG using FAISS
- Designed real-world scam detection system
- Created interactive UI with Streamlit

⚠️ Limitations

- Depends on LLM accuracy
- Limited RAG dataset
- Requires internet for API

🔮 Future Improvements

- Add real-time SMS/email detection
- Expand scam dataset
- Add voice scam detection
- Mobile app integration

👩‍💻 Author

Vandana S
1st year B.Tech CSE(core) Student

⭐ Conclusion

This project demonstrates how Agentic AI + RAG can be used to solve real-world cybersecurity problems like scam detection with an interactive and intelligent system.