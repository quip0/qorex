from pathlib import Path
from qorex.models import Language

_EXT_MAP = {
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


def detect_language(filepath: str) -> Language:
    return _EXT_MAP.get(Path(filepath).suffix.lower(), Language.UNKNOWN)
