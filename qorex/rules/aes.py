from qorex.models import Language, RiskLevel
from qorex.rules.base import Rule


class AES128Rule(Rule):
    algorithm = "AES-128"
    risk_level = RiskLevel.HIGH
    languages = []
    explanation = "AES-128 provides only ~64-bit effective security against Grover's algorithm on a quantum computer. CNSA 2.0 requires AES-256."
    migration_note = "Upgrade to AES-256. Per CNSA 2.0, AES-256 is the approved symmetric cipher."
    replacement_algorithm = "AES-256"
    patterns = [
        r"AES.{0,5}128",
        r"algorithms\.AES\b",          # cryptography lib with 128-bit key — needs key-length check
        r"AES\.new\(",                  # PyCryptodome — key length determines bit size
        r"Cipher\.getInstance\([\"']AES/",
        r"EVP_aes_128",
        r"aes\.NewCipher\(",            # Go — key length determines bit size
    ]
