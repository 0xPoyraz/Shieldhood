# Shieldhood - AI Security Skill for Bankr.bot

**Advanced AI Security Layer for autonomous DeFi agents on Robinhood Chain.**

## Description
Shieldhood acts as the **last line of defense** at the AI level. It protects autonomous DeFi agents from prompt injection, jailbreaks, obfuscated attacks, and malicious commands that could lead to unauthorized transfers or dangerous executions.

## Key Features (v2.1)
- Deep multi-layer detection with recursive payload decoding (Base64, Hex, ROT-N, entropy, invisible Unicode, etc.)
- Human confirmation gate for high-risk actions (`/shieldhood confirm`)
- Configurable spending policy (daily & per-transaction limits)
- Address allowlist support
- State persistence (daily spend tracking + pending actions)
- YAML-based configuration
- Lightweight & fast (pure Python, minimal dependencies)

## Available Commands
- `/shieldhood scan <text>` → Run full security scan
- `/shieldhood confirm` → Approve pending high-risk action
- `/shieldhood cancel` → Cancel pending action
- `/shieldhood status` → Show shield status and limits (coming soon in v2.2)
- `/shieldhood help` → Display command list

## Integration with Bankr.bot

```python
from shieldhood.guard import Shieldhood

# Initialize the shield (usually during skill loading)
shield = Shieldhood(config_path="bankr.config.yaml")

# Inside your main command handler
def handle_user_command(command: str, context: dict = None):
    # Route Shieldhood commands
    if command.startswith("/shieldhood"):
        return shield.handle_command(command, context)
    
    # Optional: Auto-scan every incoming command/prompt
    scan_result = shield.scan(command)
    if scan_result["requires_confirmation"]:
        # Block and request human confirmation
        return "🛡️ Shieldhood detected potential risk. Use /shieldhood confirm to proceed."
    
    # Continue with normal Bankr.bot logic...
```

## Setup
```bash
# Copy example config
cp bankr.config.yaml.example bankr.config.yaml

# Edit according to your risk tolerance
```

## Requirements
- Python 3.10+
- PyYAML (`pip install pyyaml`)
- Bankr.bot skill environment

## Links
- **GitHub**: https://github.com/0xPoyraz/Shieldhood
- **PyPI**: https://pypi.org/project/shieldhood/
- **Website & Live Demo**: https://www.shieldhood.xyz/
- **Official X**: [@shieldhood](https://x.com/shieldhood)
- **Developer**: [@0xPoyraz](https://x.com/0xPoyraz)

---

**Shieldhood — Securing the future of autonomous DeFi agents.**
```

---
