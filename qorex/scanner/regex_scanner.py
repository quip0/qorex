from typing import List

from qorex.models import Finding, Language
from qorex.rules.registry import get_rules_for_language


def scan_regex(filepath: str, lang: Language) -> List[Finding]:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    findings: List[Finding] = []
    rules = get_rules_for_language(lang)
    seen: set = set()

    for lineno, line in enumerate(lines, start=1):
        for rule in rules:
            match = rule.match_line(line, lineno, filepath)
            if match:
                key = (match.file, match.line, match.algorithm)
                if key not in seen:
                    seen.add(key)
                    match.language = lang
                    findings.append(match)

    return findings
