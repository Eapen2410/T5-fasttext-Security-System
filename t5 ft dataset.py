import re
import pandas as pd

sensitive_keywords = [
    "password", "otp", "pin", "account number", "phone", "number", "email",
    "username", "token", "secret", "cvv", "access key", "code"
]
mask_patterns = {
    r'[\w\.-]+@[\w\.-]+': 'xxxxx@xxxx.com',
    r'\b\d{5,}\b': 'xxxxxx',
    r'(password|otp|pin|cvv|code):?\s*\d+': r'\1: xxxxxx',
    r'access token:?\s*\w+': 'access token: xxxxxx',
    r'secret:?\s*\w+': 'secret: xxxxxx',
    r'(phone number|account number):?\s*\d+': r'\1: xxxxxx'
}

def is_sensitive(line):
    text = line.lower()
    return any(keyword in text for keyword in sensitive_keywords)

def mask_sensitive(text):
    original = text
    for pattern, repl in mask_patterns.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text if text != original else None

input_lines = []
target_lines = []

with open("fasttext_train.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line.startswith("__label__high"):
            continue
        query = line.replace("__label__high", "").strip()
        if not is_sensitive(query):
            continue
        masked = mask_sensitive(query)
        if masked:
            input_lines.append(query)
            target_lines.append(masked)

df = pd.DataFrame({
    "input_text": input_lines,
    "target_text": target_lines
})
df.to_csv("t5_sensitive_rephrase_cleaned.csv", index=False)
