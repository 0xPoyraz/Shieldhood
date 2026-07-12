<p align="center">
  <img src="https://iili.io/C1SB5a2.md.jpg" alt="Shieldhood Logo" width="220">
</p>

<h1 align="center">🛡️ Shieldhood</h1>

<p align="center">
  <strong>Advanced AI Security Layer for Bankr.bot on Robinhood Chain</strong><br>
  Protecting autonomous DeFi agents from prompt injection and malicious commands.
</p>

---

### ✨ Key Features

- **Multi-Layer Detection Engine** — Detects Base64, Hex, ROT-N, Morse, invisible Unicode, Zalgo, high-entropy payloads, and injection keywords
- **Deep Payload Analysis** — Automatically decodes obfuscated inputs then re-scans the plaintext
- **Human Confirmation Gate** — Blocks high-risk actions until manual approval
- **Spending Policy Engine** — Configurable daily and per-transaction USD limits
- **Address Allowlist** — Restrict all transactions to trusted addresses only
- **Lightweight & Production Ready** — Pure Python with zero heavy dependencies

---

### Quick Start

```bash
git clone https://github.com/linelaramee/Shieldhood.git
cd Shieldhood
python3 guard.py --self-test
