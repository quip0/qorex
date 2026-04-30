from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class DHRule(Rule):
    algorithm = "DH"
    risk_level = RiskLevel.CRITICAL
    languages = []
    explanation = "Diffie-Hellman key exchange relies on the discrete logarithm problem, which is broken by Shor's algorithm."
    migration_note = "Replace with ML-KEM (CRYSTALS-Kyber) per NIST FIPS 203."
    replacement_algorithm = "ML-KEM"
    patterns = [
        r"\bDiffie.?Hellman\b",
        r"dh\.generate_parameters",
        r"DH_generate_key",
        r"DH_new",
        r"crypto/dh",
        r"KeyAgreement\.getInstance\([\"']DH[\"']\)",
        r"\bDHE\b",
        r"_DHE_",
    ]
