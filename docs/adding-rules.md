# Adding Detection Rules

Qorex's detection engine is rule-based and designed to be extended. Adding support for a new algorithm or a new library signature takes about 15 lines of Python.

---

## How rules work

Each rule is a class that inherits from `Rule` (`qorex/rules/base.py`). It declares:

- The algorithm name and risk level
- Which languages it applies to (empty list = all languages)
- A list of regex patterns matched against each line of source code
- Plain-English explanation and migration guidance shown to the user

The registry (`qorex/rules/registry.py`) instantiates all rules and filters them by language when scanning a file.

---

## Step 1 — Create a rule file

Add a new file in `qorex/rules/`. Here is a minimal example for a hypothetical new algorithm:

```python
# qorex/rules/elgamal.py
from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class ElGamalRule(Rule):
    algorithm = "ElGamal"
    risk_level = RiskLevel.CRITICAL
    languages = []  # empty = applies to all languages
    explanation = (
        "ElGamal encryption relies on the discrete logarithm problem, "
        "which is broken by Shor's algorithm on a quantum computer."
    )
    migration_note = "Replace with ML-KEM (CRYSTALS-Kyber) per NIST FIPS 203."
    replacement_algorithm = "ML-KEM"
    patterns = [
        r"\bElGamal\b",
        r"elgamal\.encrypt",
        r"ElGamal_encrypt",
    ]
```

**Pattern tips:**

- Use `\b` word boundaries to avoid matching substrings (e.g. `\bRSA\b` won't match `PRSA`)
- Patterns are matched case-insensitively (`re.IGNORECASE`)
- Each pattern is tried independently — the first match on a line produces one finding
- Keep patterns specific enough to avoid flagging comments and documentation in unrelated projects

---

## Step 2 — Register the rule

Open `qorex/rules/registry.py` and add your rule to the imports and the `_ALL_RULES` list:

```python
from qorex.rules import rsa, ecc, dsa, dh, aes, sha, elgamal  # add elgamal

_ALL_RULES: List[Rule] = [
    rsa.RSARule(),
    ecc.ECDHRule(),
    ecc.ECDSARule(),
    dsa.DSARule(),
    dh.DHRule(),
    aes.AES128Rule(),
    sha.SHA256Rule(),
    elgamal.ElGamalRule(),  # add this
]
```

---

## Step 3 — Add tests

Add a test to `tests/rules/test_rules.py`:

```python
from qorex.rules.elgamal import ElGamalRule

def test_elgamal_rule_matches():
    rule = ElGamalRule()
    assert _hit(rule, "cipher = elgamal.encrypt(pub_key, message)")
    assert _hit(rule, "ElGamal_encrypt(ctx, msg, len, key)")
    assert not _hit(rule, "kyber.encapsulate(pub_key)")

def test_elgamal_is_critical():
    assert ElGamalRule().risk_level == RiskLevel.CRITICAL
```

Run tests:

```bash
pytest tests/rules/test_rules.py -v
```

---

## Language-specific rules

To restrict a rule to one or more languages, set the `languages` field:

```python
class SomeJavaRule(Rule):
    languages = [Language.JAVA]
    ...
```

Available language values: `Language.PYTHON`, `Language.C`, `Language.CPP`, `Language.GO`, `Language.JAVA`

---

## Rule fields reference

| Field | Type | Required | Description |
|---|---|---|---|
| `algorithm` | `str` | Yes | Short name shown in the findings table (e.g. `"RSA"`) |
| `risk_level` | `RiskLevel` | Yes | `RiskLevel.CRITICAL` or `RiskLevel.HIGH` |
| `languages` | `List[Language]` | Yes | Languages this rule applies to; `[]` means all |
| `explanation` | `str` | Yes | Plain-English explanation of why this is vulnerable |
| `migration_note` | `str` | Yes | What to replace it with, including NIST reference |
| `replacement_algorithm` | `str` | Yes | Short name of the replacement (shown in detail panel) |
| `patterns` | `List[str]` | Yes | Regex patterns matched against each source line |

---

## Keeping false positive rates low

A few guidelines that keep Qorex's false positive rate under 5%:

- **Prefer function/method names over bare algorithm names.** `rsa.generate_private_key` is more precise than `RSA` alone. Include both if the bare name is common in real code.
- **Test against clean files.** After writing a rule, run it against a codebase that you know doesn't use the algorithm and verify there are no spurious matches.
- **Avoid over-broad patterns.** A pattern like `\bkey\b` would match far too many things. Patterns should identify a specific API call, constant, or import.
- **Use word boundaries.** `\bDSA\b` won't match `ECDSA` or `DSAKey`. Without word boundaries, shorter algorithm names can produce unexpected matches.
