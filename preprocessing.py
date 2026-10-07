import re
import string

def clean_text(text: str) -> str:
    """Basic cleaning: lowercase, strip URLs/HTML/punctuation/numbers."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<.*?>', ' ', text)                 # remove HTML tags
    text = re.sub(r'http\S+|www\.\S+', ' URLTOKEN ', text)  # replace URLs with a token (keep the signal, drop the noise)
    text = re.sub(r'\S+@\S+', ' EMAILTOKEN ', text)     # replace email addresses
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', ' NUMTOKEN ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text