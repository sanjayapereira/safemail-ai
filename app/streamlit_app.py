import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predictor import predict_email

st.set_page_config(page_title="SafeMail-AI", page_icon="🛡️")

st.title("SafeMail-AI: Phishing Email Detector")
st.write("Paste an email's content below to check whether it's phishing or legitimate.")

email_text = st.text_area("Email content", height=250, placeholder="Paste subject + body here...")

if st.button("Analyze Email"):
    if not email_text.strip():
        st.warning("Please paste some email content first.")
    else:
        result = predict_email(email_text)

        if result["final_label"] == "Phishing":
            st.error(f"⚠️ This email is likely **PHISHING**")
        else:
            st.success(f"✅ This email looks **LEGITIMATE**")

        st.subheader("Details")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ML Model Verdict", result["ml_prediction"])
            st.metric("ML Confidence (phishing)", f"{result['ml_confidence']*100:.1f}%")
        with col2:
            st.metric("Rule-Based Flag", "Yes" if result["rule_indicators"]["rule_based_flag"] else "No")
            st.metric("Rule Score", result["rule_indicators"]["rule_based_score"])

        st.subheader("Indicators Detected")
        ri = result["rule_indicators"]
        if ri["suspicious_keywords"]:
            st.write("**Suspicious keywords:**", ", ".join(ri["suspicious_keywords"]))
        if ri["urgency_language"]:
            st.write("**Urgency language:**", ", ".join(ri["urgency_language"]))
        if ri["sensitive_info_request"]:
            st.write("**Sensitive info requests:**", ", ".join(ri["sensitive_info_request"]))
        if ri["suspicious_urls"]:
            st.write("**Suspicious URLs:**", ", ".join(ri["suspicious_urls"]))
        if not any([ri["suspicious_keywords"], ri["urgency_language"], ri["sensitive_info_request"], ri["suspicious_urls"]]):
            st.write("No rule-based indicators triggered.")

st.caption("SafeMail-AI does not store any submitted email content.")