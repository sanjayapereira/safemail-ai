import re

SUSPICIOUS_KEYWORDS = [
    "verify your account", "update your account", "confirm your identity",
    "suspended", "unusual activity", "click here", "act now",
    "limited time", "your account will be closed", "wire transfer",
    "gift card", "tax refund", "prize", "winner", "urgent action required"
]

URGENT_PHRASES = [
    "urgent", "immediately", "act now", "within 24 hours",
    "final notice", "account will be locked", "expires today"
]

SENSITIVE_INFO_PHRASES = [
    "password", "ssn", "social security", "credit card number",
    "bank account", "pin number", "login credentials", "otp"
]

def check_suspicious_keywords(text: str):
    text = text.lower()
    return [kw for kw in SUSPICIOUS_KEYWORDS if kw in text]

def check_urgency(text: str):
    text = text.lower()
    return [p for p in URGENT_PHRASES if p in text]

def check_sensitive_info_request(text: str):
    text = text.lower()
    return [p for p in SENSITIVE_INFO_PHRASES if p in text]

def check_suspicious_urls(text: str):
    """Flags raw IP-based links, excessive subdomains, or link-shorteners."""
    urls = re.findall(r'http\S+|www\.\S+', text.lower())
    flags = []
    shorteners = ["bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly"]
    for url in urls:
        if re.search(r'https?://\d+\.\d+\.\d+\.\d+', url):
            flags.append(f"IP-based URL: {url}")
        elif any(s in url for s in shorteners):
            flags.append(f"Shortened URL: {url}")
        elif url.count('.') >= 4:
            flags.append(f"Suspicious subdomain structure: {url}")
    return flags

def apply_rules(raw_text: str) -> dict:
    """
    Runs on the RAW (uncleaned) text so URLs and exact phrases are still intact.
    Returns a dict of triggered indicators + a simple rule-based risk score.
    """
    indicators = {
        "suspicious_keywords": check_suspicious_keywords(raw_text),
        "urgency_language": check_urgency(raw_text),
        "sensitive_info_request": check_sensitive_info_request(raw_text),
        "suspicious_urls": check_suspicious_urls(raw_text),
    }
    score = sum(len(v) for v in indicators.values())
    indicators["rule_based_flag"] = score >= 2  # e.g. IF 2+ signals THEN flag as suspicious
    indicators["rule_based_score"] = score
    return indicators