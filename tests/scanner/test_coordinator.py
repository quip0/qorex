import os
import tempfile
import pytest
from qorex.scanner.coordinator import scan_path
from qorex.models import RiskLevel


def write_temp(suffix: str, content: str):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
    f.write(content)
    f.close()
    return f.name


def test_scan_finds_rsa_python():
    path = write_temp(".py", "from cryptography.hazmat.primitives.asymmetric import rsa\nkey = rsa.generate_private_key(65537, 2048)\n")
    try:
        findings = scan_path(os.path.dirname(path))
        matched = [f for f in findings if f.algorithm == "RSA" and f.file == path]
        assert matched, "Expected RSA finding in Python file"
        assert matched[0].risk_level == RiskLevel.CRITICAL
    finally:
        os.unlink(path)


def test_scan_finds_ecdsa_c():
    path = write_temp(".c", "#include <openssl/ecdsa.h>\nECDSA_sign(0, hash, len, sig, &siglen, key);\n")
    try:
        findings = scan_path(os.path.dirname(path))
        matched = [f for f in findings if f.algorithm == "ECDSA" and f.file == path]
        assert matched, "Expected ECDSA finding in C file"
    finally:
        os.unlink(path)


def test_scan_finds_sha256_go():
    path = write_temp(".go", 'import "crypto/sha256"\nh := sha256.New()\n')
    try:
        findings = scan_path(os.path.dirname(path))
        matched = [f for f in findings if f.algorithm == "SHA-256" and f.file == path]
        assert matched, "Expected SHA-256 finding in Go file"
        assert matched[0].risk_level == RiskLevel.HIGH
    finally:
        os.unlink(path)


def test_scan_clean_file():
    path = write_temp(".py", 'import hashlib\nh = hashlib.sha512(b"data")\n')
    try:
        findings = scan_path(os.path.dirname(path))
        assert not [f for f in findings if f.file == path], "Expected no findings for SHA-512 code"
    finally:
        os.unlink(path)


def test_scan_skips_venv(tmp_path):
    venv_dir = tmp_path / ".venv" / "lib"
    venv_dir.mkdir(parents=True)
    bad_file = venv_dir / "rsa_code.py"
    bad_file.write_text("import rsa\nkey = rsa.generate_private_key()\n")
    findings = scan_path(str(tmp_path))
    assert not findings, "Should skip .venv directory"
