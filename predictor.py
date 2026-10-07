import pickle
from preprocessing import clean_text
from rule_based import apply_rules

with open("models/nb_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def predict_email(raw_text: str) -> dict:
    # Rule-based check (runs on raw text so URLs/phrases stay intact)
    rule_result = apply_rules(raw_text)

    # ML check (runs on cleaned text)
    cleaned = clean_text(raw_text)
    vec = vectorizer.transform([cleaned])
    ml_prediction = model.predict(vec)[0]
    ml_proba = model.predict_proba(vec)[0][1]  # probability of phishing

    # Combine: final verdict is "Phishing" if EITHER the model OR the rules
    # strongly indicate phishing — this is your hybrid system in action
    final_label = "Phishing" if (ml_prediction == 1 or rule_result["rule_based_flag"]) else "Legitimate"

    return {
        "final_label": final_label,
        "ml_prediction": "Phishing" if ml_prediction == 1 else "Legitimate",
        "ml_confidence": round(float(ml_proba), 3),
        "rule_indicators": rule_result,
    }