from typing import List
from qorex.models import Language
from qorex.rules.base import Rule
from qorex.rules import rsa, ecc, dsa, dh, aes, sha


_ALL_RULES: List[Rule] = [
    rsa.RSARule(),
    ecc.ECDHRule(),
    ecc.ECDSARule(),
    dsa.DSARule(),
    dh.DHRule(),
    aes.AES128Rule(),
    sha.SHA256Rule(),
]


def get_rules_for_language(lang: Language) -> List[Rule]:
    return [r for r in _ALL_RULES if not r.languages or lang in r.languages]


def get_all_rules() -> List[Rule]:
    return list(_ALL_RULES)
