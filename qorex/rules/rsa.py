from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class RSARule(Rule):
    algorithm = "RSA"
    risk_level = RiskLevel.CRITICAL
    languages = []  # applies to all languages
    explanation = "RSA is broken by Shor's algorithm on a sufficiently powerful quantum computer. Key sizes up to 4096-bit are vulnerable."
    migration_note = "Replace with ML-KEM (CRYSTALS-Kyber) for key encapsulation or ML-DSA (CRYSTALS-Dilithium) for signatures per NIST FIPS 203/204."
    replacement_algorithm = "ML-KEM / ML-DSA"
    patterns = [
        r"\bRSA\b",
        r"rsa\.generate_private_key",
        r"rsa\.RSA",
        r"RSA_generate_key",
        r"RSA_new",
        r"crypto/rsa",
        r"java\.security\.interfaces\.RSAKey",
        r"KeyPairGenerator\.getInstance\([\"']RSA[\"']\)",
    ]
