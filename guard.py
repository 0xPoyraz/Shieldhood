import re
import base64
import math

VERSION = "1.0.0"

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    entropy = -sum((count / len(text)) * math.log2(count / len(text)) for count in freq.values())
    return entropy

def scan(text: str):
    score = 0
    findings = []
    lower = text.lower()

    # Injection keywords
    if any(kw in lower for kw in ["ignore all previous", "override", "jailbreak", "transfer all", "send all"]):
        score += 50
        findings.append("INJECTION_DETECTED")

    # Base64 detection
    if re.search(r'[A-Za-z0-9+/]{30,}={0,2}', text):
        score += 30
        findings.append("BASE64_PAYLOAD")

    # High entropy
    if calculate_entropy(text) > 4.5:
        score += 25
        findings.append("HIGH_ENTROPY")

    verdict = "MALICIOUS" if score >= 60 else "SUSPICIOUS" if score >= 25 else "CLEAN"

    return {
        "verdict": verdict,
        "score": score,
        "findings": findings
    }

def handle_command(cmd: str, context=None):
    if cmd.startswith("/shieldhood scan"):
        text = cmd[15:].strip()
        result = scan(text)
        return f"🛡️ Shieldhood Scan\nVerdict: {result['verdict']}\nScore: {result['score']}/100\nFindings: {result['findings']}"
    return "🛡️ Shieldhood is ready to protect your agent on Robinhood Chain."

if __name__ == "__main__":
    print(f"✅ Shieldhood v{VERSION} ready to guard!")
