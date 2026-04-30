import os
from pathlib import Path
from typing import List

from qorex.models import Finding, Language
from qorex.scanner.language_detector import detect_language
from qorex.scanner.python_scanner import scan_python
from qorex.scanner.regex_scanner import scan_regex

SCANNERS = {
    Language.PYTHON: scan_python,
    Language.C: scan_regex,
    Language.CPP: scan_regex,
    Language.GO: scan_regex,
    Language.JAVA: scan_regex,
}

EXTENSIONS = {
    ".py": Language.PYTHON,
    ".c": Language.C,
    ".h": Language.C,
    ".cpp": Language.CPP,
    ".cc": Language.CPP,
    ".cxx": Language.CPP,
    ".hpp": Language.CPP,
    ".go": Language.GO,
    ".java": Language.JAVA,
}

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".tox", "dist", "build"}


def scan_path(root: str) -> List[Finding]:
    findings: List[Finding] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            ext = Path(filename).suffix.lower()
            if ext not in EXTENSIONS:
                continue
            lang = EXTENSIONS[ext]
            filepath = os.path.join(dirpath, filename)
            scanner = SCANNERS.get(lang, scan_regex)
            try:
                findings.extend(scanner(filepath, lang))
            except Exception:
                pass
    return findings
