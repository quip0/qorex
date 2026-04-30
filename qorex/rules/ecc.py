from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class ECDHRule(Rule):
    algorithm = "ECDH"
    risk_level = RiskLevel.CRITICAL
    languages = []
    explanation = "ECDH key exchange relies on elliptic curve discrete logarithm, which is broken by Shor's algorithm on a quantum computer."
    migration_note = "Replace with ML-KEM (CRYSTALS-Kyber) per NIST FIPS 203."
    replacement_algorithm = "ML-KEM"
    patterns = [
        r"\bECDH\b",
        r"ec\.ECDH",
        r"ECDH_compute_key",
        r"elliptic\.P-256",
        r"elliptic\.P-384",
        r"ecdh\.GenerateKey",
    ]


class ECDSARule(Rule):
    algorithm = "ECDSA"
    risk_level = RiskLevel.CRITICAL
    languages = []
    explanation = "ECDSA digital signatures rely on elliptic curve discrete logarithm, which is broken by Shor's algorithm."
    migration_note = "Replace with ML-DSA (CRYSTALS-Dilithium) or SLH-DSA (SPHINCS+) per NIST FIPS 204/205."
    replacement_algorithm = "ML-DSA / SLH-DSA"
    patterns = [
        r"\bECDSA\b",
        r"ec\.ECDSA",
        r"ECDSA_sign",
        r"ecdsa\.Sign",
        r"crypto/ecdsa",
        r"Signature\.getInstance\([\"']SHA.*withECDSA[\"']\)",
    ]
