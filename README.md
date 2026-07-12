<p align="center">
  <img src="https://iili.io/C1SB5a2.md.jpg" alt="Shieldhood Logo" width="220">
</p>

<h1 align="center">🛡️ Shieldhood</h1>

<p align="center">
  <strong>Advanced AI Security Layer for Bankr.bot on Robinhood Chain</strong><br>
  Real-time protection against prompt injection, jailbreaks, and malicious commands for autonomous DeFi agents.
</p>

---

### ✨ Key Features

- **Multi-Layer Detection Engine** — Base64, Hex, ROT-N, Morse, invisible Unicode, Zalgo, high-entropy payloads, and injection keywords
- **Deep Payload Re-scanning** — Automatically decodes obfuscated inputs then re-analyzes the plaintext
- **Human Confirmation Gate** — Blocks high-risk actions until explicit operator approval
- **Spending Policy Engine** — Configurable daily and per-transaction USD limits
- **Address Allowlist** — Restrict all transactions to trusted addresses only
- **Lightweight & Production Ready** — Pure Python with zero heavy dependencies

---

### Bankr.bot Integration
See [`SKILL.md`](SKILL.md) for detailed integration guide.

---

### Tech Stack

- **Language**: Python 3.10+
- **Core**: Pure standard library
- **Platform**: Bankr.bot Skill System
- **Chain**: Optimized for Robinhood Chain

---

### Author

**Laramée Line**  
AI Security Engineer  
[@linelaramee](https://x.com/linelaramee) | [linelaramee@gmail.com](mailto:linelaramee@gmail.com)

---

<p align="center">
  <em>Securing the future of autonomous AI agents in DeFi.</em>
</p>

### Quick Start

```bash
git clone https://github.com/linelaramee/Shieldhood.git
cd Shieldhood
python3 guard.py --self-test
