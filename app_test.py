
import streamlit as st
from PIL import Image
import cv2
import numpy as np
 
from predictor import URLPredictor
 
 
# =========================================
# PAGE CONFIG
# =========================================
 
st.set_page_config(
    page_title="QR Phishing Detector",
    page_icon="🔐",
    layout="centered"
)
 
 
# =========================================
# CUSTOM CSS
# =========================================
 
st.markdown("""
<style>
 
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
 
/* ===== ROOT ===== */
 
* { box-sizing: border-box; }
 
.stApp {
    background: #03070f;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
 
/* Subtle grid pattern overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}
 
/* ===== LAYOUT CENTERING ===== */
 
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 740px !important;
}
 
/* ===== HEADER SECTION ===== */
 
.header-wrap {
    text-align: center;
    padding: 48px 0 36px;
    position: relative;
}
 
.badge-top {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.2);
    color: #38bdf8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 20px;
}
 
.badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #38bdf8;
    animation: pulse-dot 2s ease-in-out infinite;
}
 
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}
 
.main-title {
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -1.5px;
    line-height: 1.1;
    color: #f8fafc;
    margin: 0 0 12px;
}
 
.main-title span {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
 
.subtitle {
    color: #475569;
    font-size: 15px;
    font-weight: 400;
    letter-spacing: 0.1px;
    margin: 0;
}
 
/* ===== UPLOADER ===== */
 
[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 24px;
    padding: 32px;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}
 
[data-testid="stFileUploader"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.4), transparent);
}
 
[data-testid="stFileUploader"]:hover {
    border-color: rgba(56,189,248,0.35);
}
 
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
    color: #94a3b8 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}
 
[data-testid="stFileUploaderDropzone"] {
    background: rgba(3,7,15,0.6) !important;
    border: 1px dashed rgba(56,189,248,0.2) !important;
    border-radius: 16px !important;
    padding: 28px !important;
}
 
[data-testid="stBaseButton-secondary"] {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 9px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(14,165,233,0.25) !important;
}
 
[data-testid="stBaseButton-secondary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(14,165,233,0.35) !important;
}
 
[data-testid="stFileUploaderFileName"] { color: #e2e8f0 !important; font-weight: 600 !important; }
[data-testid="stFileUploaderFileData"],
[data-testid="stFileUploaderFileData"] * { color: #64748b !important; }
[data-testid="stFileUploader"] small { color: #475569 !important; }
 
/* ===== QR IMAGE ===== */
 
[data-testid="stImage"] { text-align: center; }
 
[data-testid="stImage"] img {
    border-radius: 20px;
    padding: 12px;
    background: #ffffff;
    border: 1px solid rgba(56,189,248,0.25);
    box-shadow:
        0 0 0 1px rgba(56,189,248,0.08),
        0 20px 60px rgba(0,0,0,0.5),
        0 0 40px rgba(56,189,248,0.08);
    margin: auto;
}
 
[data-testid="stImageCaption"] {
    text-align: center;
    color: #475569 !important;
    font-size: 12px !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-top: 10px;
}
 
/* ===== SECTION LABELS ===== */
 
h2, h3,
[data-testid="stSubheader"] p,
.stSubheader p {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    color: #38bdf8 !important;
    margin: 32px 0 12px !important;
}
 
/* ===== URL BOX ===== */
 
.url-box {
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 14px;
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #7dd3fc;
    word-break: break-all;
    line-height: 1.7;
    position: relative;
}
 
.url-box::before {
    content: 'URL';
    position: absolute;
    top: -9px;
    left: 14px;
    background: #03070f;
    color: #334155;
    font-size: 10px;
    font-family: 'Inter', sans-serif;
    letter-spacing: 1px;
    font-weight: 600;
    padding: 0 6px;
}
 
/* ===== RESULT CARD — SAFE ===== */
 
.result-safe {
    position: relative;
    background: linear-gradient(135deg, rgba(5,46,22,0.9) 0%, rgba(6,78,59,0.6) 100%);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 28px 28px 24px;
    overflow: hidden;
    margin-top: 4px;
}
 
.result-safe::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
}
 
.result-safe::after {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: rgba(16,185,129,0.06);
}
 
.result-safe .result-icon {
    font-size: 38px;
    margin-bottom: 10px;
    display: block;
}
 
.result-safe h2 {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #6ee7b7 !important;
    letter-spacing: -0.3px !important;
    text-transform: none !important;
    margin: 0 0 6px !important;
}
 
.result-safe p {
    color: #a7f3d0;
    font-size: 14px;
    margin: 0;
    font-weight: 400;
    opacity: 0.85;
}
 
/* ===== RESULT CARD — PHISHING ===== */
 
.result-phishing {
    position: relative;
    background: linear-gradient(135deg, rgba(45,10,10,0.95) 0%, rgba(127,29,29,0.5) 100%);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 20px;
    padding: 28px 28px 24px;
    overflow: hidden;
    margin-top: 4px;
}
 
.result-phishing::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ef4444, #f87171, #fca5a5);
}
 
.result-phishing::after {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: rgba(239,68,68,0.06);
}
 
.result-phishing .result-icon {
    font-size: 38px;
    margin-bottom: 10px;
    display: block;
}
 
.result-phishing h2 {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #fca5a5 !important;
    letter-spacing: -0.3px !important;
    text-transform: none !important;
    margin: 0 0 6px !important;
}
 
.result-phishing p {
    color: #fecaca;
    font-size: 14px;
    margin: 0;
    font-weight: 400;
    opacity: 0.85;
}
 
/* ===== CONFIDENCE BAR ===== */
 
.confidence-wrap {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 20px 22px;
    margin-top: 14px;
}
 
.confidence-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
 
.confidence-label span:first-child {
    color: #64748b;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
 
.confidence-label span:last-child {
    color: #f8fafc;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}
 
.confidence-track {
    height: 6px;
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    overflow: hidden;
}
 
.confidence-fill-safe {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #34d399);
    border-radius: 100px;
    transition: width 0.8s ease;
}
 
.confidence-fill-danger {
    height: 100%;
    background: linear-gradient(90deg, #ef4444, #f87171);
    border-radius: 100px;
    transition: width 0.8s ease;
}
 
/* ===== THREAT BADGE ===== */
 
.threat-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
    margin-top: 14px;
}
 
.threat-high {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.3);
    color: #f87171;
}
 
.threat-medium {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
    color: #fbbf24;
}
 
.threat-low {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.25);
    color: #34d399;
}
 
.threat-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
 
.threat-dot-high { background: #ef4444; box-shadow: 0 0 6px #ef4444; }
.threat-dot-medium { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
.threat-dot-low { background: #10b981; box-shadow: 0 0 6px #10b981; }
 
/* ===== REASON BOX ===== */
 
.reason-box {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: rgba(15,23,42,0.7);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 13px 16px;
    margin-bottom: 8px;
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
    transition: border-color 0.2s ease;
}
 
.reason-box:hover {
    border-color: rgba(129,140,248,0.2);
}
 
.reason-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #818cf8;
    flex-shrink: 0;
    margin-top: 7px;
}
 
/* ===== FEATURE ITEMS ===== */
 
.feature-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}
 
.feature-safe {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(5,46,22,0.4);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    color: #86efac;
    font-weight: 500;
}
 
.feature-danger {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(45,10,10,0.5);
    border: 1px solid rgba(239,68,68,0.2);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    color: #fca5a5;
    font-weight: 500;
}
 
.feature-icon {
    font-size: 14px;
    flex-shrink: 0;
}
 
/* ===== STREAMLIT OVERRIDES ===== */
 
[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border: 1px solid !important;
}
 
/* ===== SCROLLBAR ===== */
 
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #03070f; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
 
/* ===== HIDE DEFAULTS ===== */
 
#MainMenu, footer, header { visibility: hidden; }
 
</style>
""", unsafe_allow_html=True)
 
 
# =========================================
# TITLE SECTION
# =========================================
 
st.markdown("""
<div class="header-wrap">
    <div class="badge-top">
        <span class="badge-dot"></span>
        AI-Powered Security Scanner
    </div>
    <div class="main-title">QR <span>Phishing</span><br>Detector</div>
    <p class="subtitle">Scan any QR code to instantly detect malicious URLs using machine learning</p>
</div>
""", unsafe_allow_html=True)
 
 
# =========================================
# FEATURE EXPLANATIONS
# =========================================
 
explanations = {
    0:  "Using IP Address",
    1:  "Long URL",
    2:  "Shortened URL",
    3:  "@ Symbol Usage",
    4:  "Redirecting URL",
    5:  "Hyphen in Domain",
    6:  "Too Many Subdomains",
    7:  "SSL Certificate Status",
    8:  "HTTPS Token Misuse",
    9:  "Suspicious Request URL",
    10: "URL Anchor Issue",
    11: "Suspicious HTML Tags",
    12: "Suspicious Form Handler",
    13: "Submitting to Email",
    14: "Abnormal URL Structure",
    15: "Too Many Redirects",
    16: "Mouse Hover Manipulation",
    17: "Right Click Disabled",
    18: "Iframe Usage",
}
 
 
# =========================================
# FILE UPLOAD
# =========================================
 
uploaded_file = st.file_uploader(
    "Upload a QR Code image to begin scanning",
    type=["png", "jpg", "jpeg"]
)
 
 
# =========================================
# PROCESS IMAGE
# =========================================
 
if uploaded_file is not None:
 
    image = Image.open(uploaded_file)
 
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Uploaded QR Code", width=220)
 
    image   = image.convert("RGB")
    img_np  = np.array(image, dtype=np.uint8)
    img_cv  = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
 
    detector        = cv2.QRCodeDetector()
    url, points, _  = detector.detectAndDecode(img_cv)
 
    if not url:
        st.error("❌  No QR code detected in this image.")
 
    else:
 
        # --- URL display ---
        st.subheader("Extracted URL")
        st.markdown(f'<div class="url-box">{url}</div>', unsafe_allow_html=True)
 
        # --- Predict ---
        result      = URLPredictor.predict(url)
        prediction  = result['prediction']
        features    = result['features']
        risk_score  = result['risk_score']
        reasons     = result['reasons']
 
        confidence = (
            min(95, 65 + (risk_score * 5)) if prediction == -1
            else max(85, 95 - (risk_score * 3))
        )
 
        # --- Result card ---
        st.subheader("Detection Result")
 
        if prediction == -1:
            st.markdown(f"""
            <div class="result-phishing">
                <span class="result-icon">🚨</span>
                <h2>Phishing Website Detected</h2>
                <p>This QR code leads to a URL with suspicious phishing indicators.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <span class="result-icon">✅</span>
                <h2>Safe Website</h2>
                <p>No significant phishing indicators were detected in this URL.</p>
            </div>
            """, unsafe_allow_html=True)
 
        # --- Confidence bar ---
        fill_class = "confidence-fill-danger" if prediction == -1 else "confidence-fill-safe"
        st.markdown(f"""
        <div class="confidence-wrap">
            <div class="confidence-label">
                <span>Confidence Score</span>
                <span>{confidence}%</span>
            </div>
            <div class="confidence-track">
                <div class="{fill_class}" style="width:{confidence}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # --- Threat badge ---
        if risk_score >= 7:
            st.markdown('<div class="threat-badge threat-high"><span class="threat-dot threat-dot-high"></span>Threat Level: HIGH</div>', unsafe_allow_html=True)
        elif risk_score >= 4:
            st.markdown('<div class="threat-badge threat-medium"><span class="threat-dot threat-dot-medium"></span>Threat Level: MEDIUM</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="threat-badge threat-low"><span class="threat-dot threat-dot-low"></span>Threat Level: LOW</div>', unsafe_allow_html=True)
 
       
                # --- AI Security Assistant ---

        st.subheader("AI Security Assistant")

        question = st.selectbox(
            "Ask Security Assistant",
            [
                "Why was this URL flagged?",
                "What phishing indicators were found?",
                "How dangerous is this URL?",
                "How can I stay safe?"
            ]
        )

        if question == "Why was this URL flagged?":

            st.info(
                "\n".join(
                    [f"• {reason}" for reason in reasons]
                )
            )

        elif question == "What phishing indicators were found?":

            indicators = []

            for i in range(min(len(features), len(explanations))):

                if features[i] == -1:

                    indicators.append(explanations[i])

            if indicators:

                st.warning(
                    "\n".join(
                        [f"⚠️ {item}" for item in indicators]
                    )
                )

            else:

                st.success(
                    "No phishing indicators were detected."
                )

        elif question == "How dangerous is this URL?":

            if risk_score >= 7:

                st.error(
                    f"High Risk Website\n\nRisk Score: {risk_score}/10"
                )

            elif risk_score >= 4:

                st.warning(
                    f"Medium Risk Website\n\nRisk Score: {risk_score}/10"
                )

            else:

                st.success(
                    f"Low Risk Website\n\nRisk Score: {risk_score}/10"
                )

        elif question == "How can I stay safe?":

            st.info("""
• Never enter passwords on suspicious websites

• Verify the domain name carefully

• Check for HTTPS and a valid SSL certificate

• Avoid sharing OTPs or banking information

• Close the page immediately if it appears suspicious
""")

        # --- Feature Analysis ---

        st.subheader("Feature Analysis")

        st.markdown(
            '<div class="feature-grid">',
            unsafe_allow_html=True
        )

        for i in range(min(len(features), len(explanations))):

            if features[i] == -1:

                st.markdown(
                    f'<div class="feature-danger"><span class="feature-icon">⚠</span>{explanations[i]}</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f'<div class="feature-safe"><span class="feature-icon">✓</span>{explanations[i]}</div>',
                    unsafe_allow_html=True
                )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
        