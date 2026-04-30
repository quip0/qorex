# Qorex

**Scan your codebase for quantum-vulnerable cryptography and get NIST PQC migration guidance.**

[![PyPI version](https://badge.fury.io/py/qorex.svg)](https://pypi.org/project/qorex/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

Government mandates (CNSA 2.0, CMMC) require organizations to migrate away from quantum-vulnerable cryptography by 2030. Qorex scans your codebase, tells you exactly what is vulnerable, and shows you what to replace it with — per NIST standards.

---

## Install

```bash
pip install qorex
```

---

## Two ways to use it

### Interactive TUI

```bash
qorex tui
```

A full-screen terminal interface. Type a path, press Enter to scan, then browse findings with `↑`/`↓`. The detail panel updates live as you move — algorithm, matched code, explanation, and migration guidance all in one view. All shortcuts are shown on-screen so you never need to look anything up.

```
 ██████╗  ██████╗ ██████╗ ███████╗██╗  ██╗
██╔═══██╗██╔═══██╗██╔══██╗██╔════╝╚██╗██╔╝
██║   ██║██║   ██║██████╔╝█████╗   ╚███╔╝
██║▄▄ ██║██║   ██║██╔══██╗██╔══╝   ██╔██╗
╚██████╔╝╚██████╔╝██║  ██║███████╗██╔╝ ██╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
Quantum-Vulnerability Scanner  ·  NIST PQC Migration Guidance  v0.1.0

 PATH  [./my-project___________________]  [⬡  SCAN]
 Enter scan · Tab move focus · ↑↓ browse · Ctrl+L edit path · Ctrl+S rescan · Q quit

 FINDINGS — 2 critical · 1 high        ┃  DETAIL
 ────────────────────────────────────  ┃  ─────────────────────────
 ● CRITICAL  RSA    src/auth/keys.py   ┃  ● CRITICAL
 ● CRITICAL  ECDSA  src/crypto/sign.go ┃  ALGORITHM   RSA
 ◆ HIGH      SHA-256 src/utils/hash.j  ┃  LOCATION    src/auth/keys.py : 12
                                       ┃  MATCHED CODE
                                       ┃   rsa.generate_private_key
                                       ┃  EXPLANATION
                                       ┃    RSA is broken by Shor's …
                                       ┃  MIGRATION PATH
                                       ┃    Replace with ML-KEM (FIPS 203)
                                       ┃  NIST REPLACEMENT
                                       ┃    ML-KEM / ML-DSA

 ✓ 3 finding(s)  ·  press ↑↓ to browse, Tab to move between panes
```

| Key | Action |
|---|---|
| `Enter` | Scan (when path field is focused) |
| `↑` / `↓` | Browse findings — detail updates live |
| `Tab` | Cycle focus between path, button, and table |
| `Ctrl+S` | Rescan at any time |
| `Ctrl+L` | Jump to path input |
| `Escape` | Clear detail panel |
| `Q` | Quit |

---

### CLI (non-interactive)

```bash
# Scan a directory
qorex scan ./my-project

# Scan current directory
qorex scan

# Export structured JSON with full migration guidance
qorex scan ./my-project --report json --output report.json
```

**Example output:**

```
qorex — scanned ./my-project

 Risk       Algorithm   File                        Line   Match
 ────────── ─────────── ─────────────────────────── ────── ──────────────────────
 CRITICAL   RSA         src/auth/keys.py              12   rsa.generate_private_key
 CRITICAL   ECDSA       src/crypto/sign.go            34   ecdsa.Sign
 HIGH       SHA-256     src/utils/hash.java            8   SHA-256

3 finding(s) — run with --report json for full details and migration guidance.
```

---

## What it detects

| Algorithm | Risk | Threat | NIST Replacement |
|---|---|---|---|
| RSA | CRITICAL | Shor's algorithm | ML-KEM / ML-DSA (FIPS 203/204) |
| ECDH | CRITICAL | Shor's algorithm | ML-KEM (FIPS 203) |
| ECDSA | CRITICAL | Shor's algorithm | ML-DSA / SLH-DSA (FIPS 204/205) |
| DSA | CRITICAL | Shor's algorithm | ML-DSA (FIPS 204) |
| DH / DHE | CRITICAL | Shor's algorithm | ML-KEM (FIPS 203) |
| AES-128 | HIGH | Grover's algorithm | AES-256 (CNSA 2.0) |
| SHA-256 | HIGH | Grover's algorithm | SHA-384 / SHA-512 (CNSA 2.0) |

**Languages:** Python · C · C++ · Go · Java

---

## Documentation

| Doc | Description |
|---|---|
| [Usage Guide](docs/usage.md) | CLI reference, TUI guide, JSON report format |
| [Detection Rules](docs/detection-rules.md) | Every algorithm, why it's vulnerable, and how to fix it |
| [Adding Rules](docs/adding-rules.md) | How to extend Qorex with new detection rules |

---

## Roadmap

- [ ] CBOM (Cryptographic Bill of Materials) export
- [ ] CNSA 2.0 / CMMC compliance report PDF
- [ ] CI/CD integrations (GitHub Actions, GitLab CI)
- [ ] Tree-sitter AST scanning for C/C++
- [ ] Rust and JavaScript/TypeScript support

---

## License

MIT — see [LICENSE](LICENSE).
