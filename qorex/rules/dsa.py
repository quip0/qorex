from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class DSARule(Rule):
    algorithm = "DSA"
    risk_level = RiskLevel.CRITICAL
    languages = []
    explanation = "DSA relies on the discrete logarithm problem, which is broken by Shor's algorithm on a quantum computer."
    migration_note = "Replace with ML-DSA (CRYSTALS-Dilithium) per NIST FIPS 204."
    replacement_algorithm = "ML-DSA"
    patterns = [
        r"\bDSA\b",
        r"dsa\.generate_parameters",
        r"dsa\.generate_private_key",
        r"DSA_generate_key",
        r"DSA_new",
        r"crypto/dsa",
        r"KeyPairGenerator\.getInstance\([\"']DSA[\"']\)",
    ]
