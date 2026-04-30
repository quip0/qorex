import re
from abc import ABC, abstractmethod
from typing import List, Optional
import ast

from qorex.models import Finding, Language, RiskLevel


class Rule(ABC):
    algorithm: str
    risk_level: RiskLevel
    languages: List[Language]
    explanation: str
    migration_note: str
    replacement_algorithm: str
    patterns: List[str]  # regex patterns for line-level matching

    def match_line(self, line: str, lineno: int, filepath: str) -> Optional[Finding]:
        for pattern in self.patterns:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                return Finding(
                    file=filepath,
                    line=lineno,
                    algorithm=self.algorithm,
                    risk_level=self.risk_level,
                    language=Language.UNKNOWN,
                    matched_text=m.group(0).strip(),
                    explanation=self.explanation,
                    migration_note=self.migration_note,
                    replacement_algorithm=self.replacement_algorithm,
                    code_snippet=None,
                )
        return None

    def match_ast(self, node: ast.AST, filepath: str, lines: List[str]) -> Optional[Finding]:
        return None
