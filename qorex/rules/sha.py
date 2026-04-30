from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class SHA256Rule(Rule):
    algorithm = "SHA-256"
    risk_level = RiskLevel.HIGH
    languages = []
    explanation = "SHA-256 provides only ~128-bit effective collision resistance against Grover's algorithm. CNSA 2.0 requires SHA-384 or SHA-512."
    migration_note = "Upgrade to SHA-384 or SHA-512 per CNSA 2.0."
    replacement_algorithm = "SHA-384 / SHA-512"
    patterns = [
        r"\bSHA.?256\b",
        r"hashlib\.sha256",
        r"SHA256_Init",
        r"SHA256_Update",
        r"sha256\.New\(",
        r"MessageDigest\.getInstance\([\"']SHA-256[\"']\)",
    ]
