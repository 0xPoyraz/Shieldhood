import re
import base64
import math
import yaml
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

VERSION = "2.1.0"  # Di-update

class DeepDecoder:
    """Deep payload decoding with recursive multi-layer re-scanning"""
    
    @staticmethod
    def try_decode(text: str, max_depth: int = 5) -> List[str]:
        candidates = [text]
        seen = {text}

        for _ in range(max_depth):
            new_candidates = []
            for payload in candidates:
                # Base64
                if re.search(r'[A-Za-z0-9+/]{20,}={0,2}', payload):
                    try:
                        decoded = base64.b64decode(payload.strip(), validate=False).decode('utf-8', errors='ignore')
                        if decoded not in seen:
                            seen.add(decoded)
                            new_candidates.append(decoded)
                    except:
                        pass

                # Hex
                if re.search(r'[0-9a-fA-F]{8,}', payload):
                    try:
                        clean = re.sub(r'[^0-9a-fA-F]', '', payload.lower())
                        if len(clean) % 2 == 0:
                            decoded = bytes.fromhex(clean).decode('utf-8', errors='ignore')
                            if decoded not in seen:
                                seen.add(decoded)
                                new_candidates.append(decoded)
                    except:
                        pass

                # ROT-N (13, 5, 7, 18)
                for shift in [13, 5, 7, 18]:
                    decoded = ''.join(
                        chr((ord(c) - 65 + shift) % 26 + 65) if 'A' <= c <= 'Z' else
                        chr((ord(c) - 97 + shift) % 26 + 97) if 'a' <= c <= 'z' else c
                        for c in payload
                    )
                    if decoded != payload and decoded not in seen:
                        seen.add(decoded)
                        new_candidates.append(decoded)

                # URL Decode
                try:
                    import urllib.parse
                    decoded_url = urllib.parse.unquote(payload)
                    if decoded_url != payload and decoded_url not in seen:
                        seen.add(decoded_url)
                        new_candidates.append(decoded_url)
                except:
                    pass

            if not new_candidates:
                break
            candidates.extend(new_candidates)

        return list(seen)


class Shieldhood:
    def __init__(self, config_path: str = "bankr.config.yaml", state_path: str = "shieldhood_state.json"):
        self.config = self._load_config(config_path)
        self.state_path = state_path
        self.state = self._load_state()
        
        self.pending_confirmation: Optional[str] = self.state.get("pending_confirmation")
        self.daily_spend = self.state.get("daily_spend", 0)
        self.last_reset = datetime.fromisoformat(self.state.get("last_reset", datetime.now().isoformat())).date()
        
        spending = self.config.get('spending', {})
        self.daily_limit = spending.get('daily_limit_usd', 5000)
        self.tx_limit = spending.get('tx_limit_usd', 1000)
        
        allow = self.config.get('allowlist', {})
        self.allowlist = allow.get('addresses', [])
        self.allowlist_enabled = allow.get('enabled', False)

    def _load_config(self, path: str) -> Dict:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}

    def _load_state(self) -> Dict:
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_state(self):
        state = {
            "pending_confirmation": self.pending_confirmation,
            "daily_spend": self.daily_spend,
            "last_reset": self.last_reset.isoformat()
        }
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

    def _reset_daily_if_needed(self):
        today = datetime.now().date()
        if today > self.last_reset:
            self.daily_spend = 0
            self.last_reset = today
            self._save_state()

    def calculate_entropy(self, text: str) -> float:
        if not text or len(text) < 5:
            return 0.0
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        return -sum((count / len(text)) * math.log2(count / len(text)) 
                    for count in freq.values())

    def scan(self, text: str) -> Dict[str, Any]:
        self._reset_daily_if_needed()
        score = 0
        findings: List[str] = []
        lower = text.lower()

        # Injection keywords
        injection_keywords = [
            "ignore all previous", "override", "jailbreak", "system prompt", 
            "new instructions", "forget previous", "developer mode", 
            "disregard", "you are now"
        ]
        if any(kw in lower for kw in injection_keywords):
            score += 45
            findings.append("INJECTION_KEYWORD")

        # Deep recursive decode
        decoded_versions = DeepDecoder.try_decode(text)
        for decoded in decoded_versions:
            d_lower = decoded.lower()
            if any(kw in d_lower for kw in injection_keywords):
                score += 55
                findings.append("DECODED_INJECTION")
                break

        if re.search(r'[A-Za-z0-9+/]{30,}={0,2}', text):
            score += 30
            findings.append("BASE64_PAYLOAD")

        if self.calculate_entropy(text) > 4.2:
            score += 25
            findings.append("HIGH_ENTROPY")

        if any(ord(c) > 0xE0000 or (0x2000 <= ord(c) <= 0x206F) for c in text):  # Invisible + control chars
            score += 40
            findings.append("INVISIBLE_UNICODE")

        verdict = "MALICIOUS" if score >= 60 else "SUSPICIOUS" if score >= 35 else "CLEAN"
        
        result = {
            "verdict": verdict,
            "score": min(score, 100),
            "findings": findings,
            "decoded_versions": len(decoded_versions) - 1,
            "requires_confirmation": verdict != "CLEAN"
        }
        return result

    def check_spending(self, amount_usd: float) -> Tuple[bool, str]:
        self._reset_daily_if_needed()
        if amount_usd > self.tx_limit:
            return False, f"Transaction exceeds single tx limit (${self.tx_limit})"
        if self.daily_spend + amount_usd > self.daily_limit:
            return False, f"Exceeds daily limit (remaining: ${self.daily_limit - self.daily_spend})"
        return True, "OK"

    def handle_command(self, cmd: str, context: Dict = None) -> str:
        if cmd.startswith("/shieldhood scan"):
            text = cmd[15:].strip()
            result = self.scan(text)
            if result["requires_confirmation"]:
                self.pending_confirmation = text
                self._save_state()
                return f"🛡️ Shieldhood v{VERSION}\nVerdict: {result['verdict']}\nScore: {result['score']}/100\nFindings: {result['findings']}\n\n🔐 HUMAN CONFIRMATION REQUIRED\nUse /shieldhood confirm"
            return f"🛡️ Shieldhood v{VERSION}\nVerdict: {result['verdict']}\nScore: {result['score']}/100\nFindings: {result['findings']}"

        elif cmd == "/shieldhood confirm" and self.pending_confirmation:
            self.pending_confirmation = None
            self._save_state()
            return "✅ Action confirmed and executed."

        elif cmd == "/shieldhood cancel" and self.pending_confirmation:
            self.pending_confirmation = None
            self._save_state()
            return "❌ Action cancelled."

        return f"🛡️ Shieldhood v{VERSION} is active and protecting your agent."

if __name__ == "__main__":
    shield = Shieldhood()
    print(f"✅ Shieldhood v{VERSION} ready to guard!")
