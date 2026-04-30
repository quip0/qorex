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

The TUI is the best way to explore a codebase you're not yet familiar with. It gives you a live findings list on the left and a detail panel on the right that updates as you move through the list. Everything you need to navigate is shown on-screen — you don't need to memorise any shortcuts.

### Layout

```
┌─ Banner ───────────────────────────────────────────────────────┐
│  QOREX  Quantum-Vulnerability Scanner  ·  v0.1.0               │
├─ Scan bar ─────────────────────────────────────────────────────┤
│  PATH  [./my-project____________________]  [⬡  SCAN]           │
├─ Hint bar ─────────────────────────────────────────────────────┤
│  Enter scan  ·  Tab move focus  ·  ↑↓ browse  ·  Q quit  …    │
├─ Findings (58%) ───────────────┬─ Detail (42%) ────────────────┤
│  ● CRITICAL  RSA  keys.py   12 │  ● CRITICAL                   │
│  ● CRITICAL  ECDSA  sign.go  3 │  ──────────────────────────   │
│  ◆ HIGH     SHA-256  hash.j  8 │  ALGORITHM   RSA              │
│                                │  LOCATION    src/keys.py : 12 │
│                                │  MATCHED CODE                 │
│                                │   rsa.generate_private_key    │
│                                │  EXPLANATION                  │
│                                │    RSA is broken by Shor's …  │
│                                │  MIGRATION PATH               │
│                                │    Replace with ML-KEM …      │
│                                │  NIST REPLACEMENT             │
│                                │    ML-KEM / ML-DSA            │
├────────────────────────────────┴───────────────────────────────┤
│  ✓ 3 finding(s)  ·  press ↑↓ to browse, Tab to move panes     │
└────────────────────────────────────────────────────────────────┘
```

There are five zones, stacked top to bottom with no overlap:

| Zone | Purpose |
|---|---|
| Banner | App name and version |
| Scan bar | Path input and scan button |
| Hint bar | Always-visible keyboard reference |
| Main area | Findings table (left) and detail panel (right) |
| Status bar | Contextual feedback — updates after each action |

### Keyboard shortcuts

| Key | Action |
|---|---|
| `Enter` | Scan from the current path (when path input is focused) |
| `Ctrl+S` | Rescan at any time, regardless of which pane has focus |
| `↑` / `↓` | Move through the findings list — detail updates live |
| `Tab` | Cycle focus between the path input, scan button, and findings table |
| `Ctrl+L` | Jump focus directly to the path input to type a new path |
| `Escape` | Clear the detail panel and return focus to the findings table |
| `Q` | Quit (safe — does nothing when you are typing in the path input) |

### What the detail panel shows

Each finding shows:

- **Risk level** — CRITICAL (red) or HIGH (amber)
- **Algorithm** — the vulnerable algorithm name
- **Location** — file path and line number
- **Matched code** — the exact text that triggered the detection
- **Explanation** — plain-English description of the quantum threat
- **Migration path** — what to replace it with and why
- **NIST replacement** — the specific standard (e.g. FIPS 203 ML-KEM)

The detail panel scrolls independently if the content is longer than the pane height.

### Workflow

1. Launch `qorex tui` — the path field pre-fills with `.` and is already focused
2. Edit the path if needed, then press `Enter` or click **⬡ SCAN**
3. The findings table populates and focus moves there automatically
4. Press `↑`/`↓` to browse — the detail panel updates as you move
5. Press `Ctrl+L` to edit the path, then `Enter` to re-scan a different directory
6. Press `Q` to quit when done

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
