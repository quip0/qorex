# Usage Guide

Qorex has two modes: an interactive TUI for exploring findings, and a CLI for scripting, CI/CD, and quick scans.

---

## Installation

```bash
pip install qorex
```

Requires Python 3.10 or later. No other system dependencies.

---

## TUI — Interactive Mode

```bash
qorex tui
```

The TUI is the best way to explore a codebase you're not yet familiar with. It gives you a live findings list on the left and a detail panel on the right that shows the full explanation and migration guidance for whatever finding you have selected.

### Layout

```
┌─ Banner ──────────────────────────────────────────────────────┐
│  QOREX  Quantum-Vulnerability Scanner  ◈  v0.1.0              │
├─ Scan bar ────────────────────────────────────────────────────┤
│  ◈ PATH  [./my-project_________________]  [⬡  SCAN]           │
├─ Findings (58%) ──────────────┬─ Detail (42%) ────────────────┤
│  ● CRITICAL  RSA  keys.py  12 │  ● CRITICAL                   │
│  ● CRITICAL  ECDSA  sign.go 3 │  ALGORITHM   RSA              │
│  ◆ HIGH     SHA-256  hash.j 8 │  LOCATION    src/keys.py : 12 │
│                               │  EXPLANATION                  │
│                               │    RSA is broken by Shor's …  │
│                               │  MIGRATION PATH               │
│                               │    Replace with ML-KEM …      │
│                               │  NIST REPLACEMENT             │
│                               │    ML-KEM / ML-DSA            │
├───────────────────────────────┴───────────────────────────────┤
│  ✓ Scan complete: ./my-project  ·  3 finding(s)               │
└───────────────────────────────────────────────────────────────┘
```

### Keyboard shortcuts

| Key | Action |
|---|---|
| `s` | Run a scan with the current path |
| `j` / `k` | Move down / up through findings |
| `↑` / `↓` | Same as `j` / `k` |
| `Enter` | Select highlighted finding, show detail |
| `Ctrl+O` | Jump focus to the path input |
| `Escape` | Clear the detail panel |
| `q` | Quit |

### Workflow

1. Launch `qorex tui`
2. In the path field, type the directory you want to scan (defaults to `.`)
3. Press `Enter` or click **SCAN**
4. Use `j`/`k` to move through the findings list
5. Press `Enter` on any row to read the full explanation and migration guidance in the right panel
6. Edit the path and scan again — the table refreshes in place

---

## CLI — Non-interactive Mode

### Basic scan

```bash
qorex scan ./my-project
```

Scans `./my-project` recursively and prints a table to stdout. Exits 0 whether or not findings exist.

```bash
# Scan the current directory
qorex scan
```

### JSON report

```bash
qorex scan ./my-project --report json
```

Prints structured JSON to stdout.

```bash
qorex scan ./my-project --report json --output report.json
```

Writes the report to `report.json` instead.

### JSON report format

```json
{
  "version": "0.1.0",
  "findings": [
    {
      "file": "src/auth/keys.py",
      "line": 12,
      "algorithm": "RSA",
      "risk_level": "critical",
      "language": "python",
      "matched_text": "rsa.generate_private_key",
      "explanation": "RSA is broken by Shor's algorithm ...",
      "migration_note": "Replace with ML-KEM (CRYSTALS-Kyber) ...",
      "replacement_algorithm": "ML-KEM / ML-DSA",
      "code_snippet": null
    }
  ],
  "summary": {
    "total": 3,
    "critical": 2,
    "high": 1
  }
}
```

### Version

```bash
qorex --version
```

---

## Scanned languages

Qorex automatically detects language from the file extension:

| Extension | Language | Scanner |
|---|---|---|
| `.py` | Python | Regex over source lines |
| `.c`, `.h` | C | Regex |
| `.cpp`, `.cc`, `.cxx`, `.hpp` | C++ | Regex |
| `.go` | Go | Regex |
| `.java` | Java | Regex |

Files with other extensions are skipped. The following directories are always excluded:

`.git` · `.venv` · `venv` · `node_modules` · `__pycache__` · `.tox` · `dist` · `build`

---

## CI/CD integration

Qorex works in any CI pipeline that has Python available. Example GitHub Actions step:

```yaml
- name: Scan for quantum-vulnerable cryptography
  run: |
    pip install qorex
    qorex scan . --report json --output qorex-report.json

- name: Upload report
  uses: actions/upload-artifact@v4
  with:
    name: qorex-report
    path: qorex-report.json
```

To fail the build on any critical finding, pipe through `jq`:

```bash
qorex scan . --report json | jq -e '.summary.critical == 0'
```

---

## False positives

Qorex uses regex pattern matching, which means it can flag algorithm names that appear in comments, string literals, or variable names that reference deprecated code you are actively removing.

If a finding is a false positive, the recommended approach is to add a suppression comment (support planned) or exclude specific directories with a config file (also on the roadmap). For now, the JSON report makes it easy to filter results programmatically.
