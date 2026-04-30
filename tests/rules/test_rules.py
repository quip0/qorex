import pytest
from qorex.models import Language, RiskLevel
from qorex.rules.rsa import RSARule
from qorex.rules.ecc import ECDHRule, ECDSARule
from qorex.rules.dsa import DSARule
from qorex.rules.dh import DHRule
from qorex.rules.aes import AES128Rule
from qorex.rules.sha import SHA256Rule


def _hit(rule, line):
    return rule.match_line(line, 1, "test.py")


def test_rsa_rule_matches():
    rule = RSARule()
    assert _hit(rule, "key = rsa.generate_private_key(65537, 2048)")
    assert _hit(rule, 'KeyPairGenerator.getInstance("RSA")')
    assert not _hit(rule, "# this is safe code")


def test_ecdh_rule_matches():
    rule = ECDHRule()
    assert _hit(rule, "peer = ec.ECDH(curve=SECP256R1())")
    assert not _hit(rule, "ml_kem.generate_key()")


def test_ecdsa_rule_matches():
    rule = ECDSARule()
    assert _hit(rule, 'sig = Signature.getInstance("SHA256withECDSA")')
    assert _hit(rule, "ECDSA_sign(0, digest, dlen, sig, &slen, key)")


def test_dsa_rule_matches():
    rule = DSARule()
    assert _hit(rule, "params = dsa.generate_parameters(key_size=2048)")
    assert not _hit(rule, "dilithium.sign(msg)")


def test_dh_rule_matches():
    rule = DHRule()
    assert _hit(rule, "params = dh.generate_parameters(generator=2, key_size=2048)")
    assert _hit(rule, "cipher_suite = TLS_DHE_RSA_WITH_AES_256")


def test_aes128_rule_matches():
    rule = AES128Rule()
    assert _hit(rule, "EVP_aes_128_cbc()")
    assert _hit(rule, "AES-128-CBC")
    assert not _hit(rule, "AES-256-GCM")


def test_sha256_rule_matches():
    rule = SHA256Rule()
    assert _hit(rule, "h = hashlib.sha256(data)")
    assert _hit(rule, 'MessageDigest.getInstance("SHA-256")')
    assert not _hit(rule, "h = hashlib.sha512(data)")


def test_all_critical_rules_have_correct_risk():
    for rule in [RSARule(), ECDHRule(), ECDSARule(), DSARule(), DHRule()]:
        assert rule.risk_level == RiskLevel.CRITICAL


def test_all_high_rules_have_correct_risk():
    for rule in [AES128Rule(), SHA256Rule()]:
        assert rule.risk_level == RiskLevel.HIGH
