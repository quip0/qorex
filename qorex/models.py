from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RiskLevel(str, Enum):
    CRITICAL = "critical"   # broken by Shor (RSA, ECC, DSA, DH, ECDH, ECDSA)
    HIGH = "high"           # weakened by Grover (AES-128, SHA-256)


class Language(str, Enum):
    PYTHON = "python"
    C = "c"
    CPP = "cpp"
    GO = "go"
    JAVA = "java"
    UNKNOWN = "unknown"


@dataclass
class Finding:
    file: str
    line: int
    algorithm: str
    risk_level: RiskLevel
    language: Language
    matched_text: str
    explanation: str
    migration_note: str
    replacement_algorithm: str
    code_snippet: Optional[str] = None
