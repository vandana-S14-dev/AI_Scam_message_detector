import streamlit as st
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq
import os
import json

import re

def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

# -----------------------------
# API CONFIG (SECURE)
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# RAG DATABASE
# -----------------------------
scam_data = [
    "You won a lottery! Click to claim prize",
    "Share OTP to verify account",
    "Urgent: bank account will be blocked",
    "Job requires upfront payment",
    "Click link to update KYC immediately",
    "Your card is suspended, login now"
]

# -----------------------------
# EMBEDDINGS + FAISS
# -----------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = embed_model.encode(scam_data)

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(np.array(vectors))


def retrieve_rag(text):
    q_vec = embed_model.encode([text])
    _, idx = index.search(np.array(q_vec), k=2)
    return [scam_data[i] for i in idx[0]]


# -----------------------------
# LLM CALL
# -----------------------------
def call_LLM(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a cybersecurity AI that detects scams."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"API Error: {str(e)}"


# -----------------------------
# AGENTS
# -----------------------------
def pattern_agent(text, context):
    prompt = f"""
Analyze the message carefully.

If it contains scam indicators, list them.
If it looks normal/safe, say: "No scam patterns detected".

Message: {text}
Similar cases: {context}

Return bullet points starting with '-'
"""
    return call_LLM(prompt)


def risk_agent(patterns):
    prompt = f"""
You are a security classifier.

If patterns show no scam → risk must be LOW.

Return ONLY JSON:

{{"risk_score": number, "label": "Low/Medium/High"}}

Rules:
- No scam → score < 30
- Suspicious → 30-70
- Clear scam → > 70

Patterns:
{patterns}
"""
    return call_LLM(prompt)


def reasoning_agent(text, patterns):
    prompt = f"""
Explain why this is a scam.

Return ONLY bullet points starting with '-'

Message: {text}
Patterns: {patterns}
"""
    return call_LLM(prompt)


def advice_agent(risk):
    prompt = f"""
Give safety advice.

Return ONLY bullet points starting with '-'

Risk:
{risk}
"""
    return call_LLM(prompt)


# -----------------------------
# PIPELINE
# -----------------------------
def run_agents(text):
    context = retrieve_rag(text)
    context_str = "\n".join(context)

    pattern = pattern_agent(text, context_str)
    risk = risk_agent(pattern)
    reasoning = reasoning_agent(text, pattern)
    advice = advice_agent(risk)

    return context, pattern, risk, reasoning, advice


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="AI Scam Detector", layout="wide")

st.title("🕵️ AI Scam Detection Assistant")
st.markdown("### Agentic AI + RAG + LLM Security System")

# Input box
user_input = st.text_area("Paste suspicious message here:",
                          value=st.session_state.get("input_text", ""))

st.session_state.input_text = user_input

# Analyze button
if st.button("Analyze"):
    st.session_state.result = run_agents(user_input)

# -----------------------------
# SHOW RESULTS (PERSISTENT)
# -----------------------------
if "result" in st.session_state:

    context, pattern, risk, reasoning, advice = st.session_state.result

    st.info("🔍 Analysis Complete")

     # -------- SMART RISK FIX --------
    if "No scam patterns" in pattern:
        score = 10
        label = "Low"
    else:
        risk_json = extract_json(risk)

        if risk_json:
            score = int(risk_json.get("risk_score", 0))
            label = risk_json.get("label", "Low")
        else:
            score = 0
            label = "Error"

    # -------- Color --------
    if label == "High":
        color = "#ff4b4b"
    elif label == "Medium":
        color = "#ffa500"
    else:
        color = "#00c853"

    # -------- Layout --------
    col1, col2 = st.columns([1, 2])

    # LEFT SIDE
    with col1:
        st.subheader("🔍 RAG Results")
        for c in context:
            st.markdown(f"• {c}")

        st.subheader("⚠️ Patterns")
        for b in pattern.split("\n"):
            if b.strip():
                st.markdown(f"• {b.replace('-', '').strip()}")

    # RIGHT SIDE
    with col2:
        st.subheader("🚨 Risk Dashboard")

        # Score Card
        st.markdown(
            f"""
            <div style="padding:20px; border-radius:12px; background-color:{color}; color:white; text-align:center;">
                <h1>{score}</h1>
                <h3>{label} Risk</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Progress Bar
        st.progress(score/100)

        # Risk Meter
        st.markdown("### 📊 Risk Meter")
        if score < 40:
            st.success("🟢 Safe")
        elif score < 70:
            st.warning("🟡 Suspicious")
        else:
            st.error("🔴 Dangerous")

        # Reasoning
        st.subheader("🧠 Reasoning")
        for r in reasoning.split("\n"):
            if r.strip():
                st.markdown(f"• {r.replace('-', '').strip()}")

        # Advice
        st.subheader("🛡️ Advice")
        for a in advice.split("\n"):
            if a.strip():
                st.markdown(f"• {a.replace('-', '').strip()}")

        # Final Verdict
        st.subheader("📢 Final Verdict")

        if label == "High":
            st.error("🚨 SCAM DETECTED - Do NOT proceed")
        elif label == "Medium":
            st.warning("⚠️ SUSPICIOUS - Be cautious")
        else:
            st.success("✅ SAFE MESSAGE")

        # -----------------------------
        # USER INTERACTION CHECK
        # -----------------------------
        st.subheader("🤔 Quick Safety Check")

        clicked = st.checkbox("I clicked a link")
        shared = st.checkbox("I shared OTP/details")
        unknown = st.checkbox("Unknown sender")

        if clicked or shared:
            st.error("🚨 HIGH RISK ACTION DETECTED! Take immediate action!")

        # -----------------------------
        # EMERGENCY BUTTON
        # -----------------------------
        if st.button("🚨 What should I do NOW?"):
            st.markdown("""
            ### 🚨 Immediate Steps:
            - Contact your bank immediately
            - Block your card/account
            - Change passwords
            - Enable 2FA
            - Report cybercrime (India: 1930)
            """)

# Footer
st.markdown("---")
st.markdown("Built using Agentic AI + RAG")