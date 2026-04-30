# Qorex

**Scan your codebase for quantum-vulnerable cryptography and get NIST PQC migration guidance.**

[![PyPI version](https://badge.fury.io/py/qorex.svg)](https://pypi.org/project/qorex/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Government mandates (CNSA 2.0, CMMC) require organizations to migrate away from quantum-vulnerable cryptography by 2030. Qorex finds the vulnerable code for you and tells you exactly what to replace it with.

---

## Install

```bash
pip install qorex
```

---

## Usage

```bash
# Scan a directory
qorex scan ./my-project

# Scan current directory
qorex scan

# Export full JSON report with migration guidance
qorex scan ./my-project --report json --output report.json
```

---

## What it detects

| Algorithm | Risk | Threat | Replacement (NIST) |
|---|---|---|---|
| RSA | CRITICAL | Shor's algorithm | ML-KEM / ML-DSA (FIPS 203/204) |
| ECDH | CRITICAL | Shor's algorithm | ML-KEM (FIPS 203) |
| ECDSA | CRITICAL | Shor's algorithm | ML-DSA / SLH-DSA (FIPS 204/205) |
| DSA | CRITICAL | Shor's algorithm | ML-DSA (FIPS 204) |
| DH / DHE | CRITICAL | Shor's algorithm | ML-KEM (FIPS 203) |
| AES-128 | HIGH | Grover's algorithm | AES-256 (CNSA 2.0) |
| SHA-256 | HIGH | Grover's algorithm | SHA-384 / SHA-512 (CNSA 2.0) |

**Languages supported:** Python, C, C++, Go, Java

---

## Example output

```
qorex — scanned ./my-project

 Risk       Algorithm   File                          Line   Match
 ────────── ─────────── ───────────────────────────── ────── ──────────────────────
 CRITICAL   RSA         src/auth/keys.py               12    rsa.generate_private_key
 CRITICAL   ECDSA       src/crypto/sign.go             34    ecdsa.Sign
 HIGH       SHA-256     src/utils/hash.java            8     SHA-256

3 finding(s) — run with --report json for full details and migration guidance.
```

---

## JSON report

```bash
qorex scan . --report json --output report.json
```

Each finding includes the file, line, algorithm, risk level, plain-English explanation, NIST replacement algorithm, and migration guidance.

---

## Roadmap

- [ ] CBOM (Cryptographic Bill of Materials) export
- [ ] CNSA 2.0 / CMMC compliance reports
- [ ] CI/CD integrations (GitHub Actions, GitLab CI)
- [ ] Tree-sitter AST scanning for C/C++

---

## Contributing

Issues and PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT — see [LICENSE](LICENSE).
