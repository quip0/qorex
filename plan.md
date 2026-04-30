# Qorex

> Open-source CLI tool that scans codebases for quantum-vulnerable cryptography and generates prioritized migration guidance aligned to NIST PQC standards.

---

## The Problem

Government mandates (CNSA 2.0, CMMC) require organizations to migrate away from quantum-vulnerable cryptography (RSA, ECC, DSA) by 2030. Thousands of small defense contractors and gov IT vendors need to comply but have no affordable, developer-friendly tooling to do it. Enterprise platforms like QuSecure target Fortune 500s and federal agencies -- nobody is building for the engineers handed a compliance task with no starting point.

---

## The Opportunity

- PQC migration market: $1.9B (2025) to $12.4B (2035)
- CNSA 2.0 mandate affects $200B+ in annual defense contracting
- Underserved segment: small defense contractors, gov IT developers, CMMC Level 3 candidates
- No developer-native, open-source PQC scanning tool exists

---

## What Qorex Is

A developer-first PQC migration toolkit:
- **Free/open-source core:** CLI scanner, vulnerability detection, migration guidance, JSON export
- **Paid tier:** CBOM export, compliance reports (CNSA 2.0 / CMMC), CI/CD integrations, enterprise deployment

Monetization model: open-source flywheel -> developer adoption -> organizational compliance needs -> paid tier. Similar playbook to Snyk.

---

## Target Users

| User | Context |
|---|---|
| Developer at small defense contractor | Handed a CMMC compliance task, needs to know where to start |
| Security engineer at gov IT vendor | Needs an audit report before contract renewal |
| Curious developer / researcher | Finds it on GitHub, potential future customer |

---

## MVP Scope

**Product:** CLI tool, pip installable (pip install qorex)

**Core flow:**
1. qorex scan ./project -- recursive codebase scan
2. Findings output: file, line, algorithm, risk level, plain-English explanation
3. Per-finding migration path with NIST replacement algorithm + code snippet
4. --report json flag exports structured JSON report

**Languages (MVP):** Python (P0), C/C++ (P0), Go (P1), Java (P1)

**Algorithms detected:**
- RSA, ECDH, ECDSA, DSA, DH -- broken by Shor algorithm
- AES-128, SHA-256 -- weakened by Grover algorithm

**Out of scope for MVP:** web UI, CI/CD integrations, CBOM formal spec, auto-remediation, user accounts, paid tier, SaaS

**Tech stack:** Python, AST + regex scanning engine, tree-sitter for C/C++, Rich for terminal output, PyPI + Homebrew distribution

---

## Monetization (post-traction)

Monetize after hitting: 500+ GitHub stars, 1K+ pip installs/month, inbound compliance feature requests, 3+ companies in production.

| Tier | Price | Features |
|---|---|---|
| Free | $0 | Core scanner, all detection rules, JSON export, migration guidance |
| Developer | $99/mo | CBOM export, compliance report PDF, scan history |
| Team | $499/mo | CI/CD integrations, multi-repo dashboard, SSO |
| Enterprise | $2-5K/mo | Air-gapped deployment, audit logs, SLA, on-prem |

---

## Success Metrics (MVP)

| Metric | Target | Timeframe |
|---|---|---|
| GitHub stars | 100+ | 30 days post-launch |
| pip installs | 500+ | 60 days post-launch |
| False positive rate | < 5% | At launch |
| Scan speed | < 5s / 10K LOC | At launch |
| User interviews | 3 defense/gov devs | First 2 weeks |

---

## Longer-Term Path

1. **MVP** -- open-source CLI, organic GitHub growth
2. **Paid tier** -- compliance reports, CI/CD integrations
3. **SBIR** -- DoD SBIR proposal once paying customers exist as proof
4. **Scale** -- FedRAMP, IL4/IL5, prime contractor licensing, seed round

---

## Status

- [ ] PRD written
- [ ] GitHub repo created (qorex)
- [ ] PyPI name reserved
- [ ] Domain secured (qorex.dev or qorex.io)
- [ ] MVP build started

---

*Everything here is flexible. Update as the product evolves.*
