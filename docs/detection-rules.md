# Detection Rules

Qorex detects two categories of vulnerability, mapped directly to the two quantum algorithms that threaten classical cryptography.

---

## Why quantum computers break crypto

**Shor's algorithm** can factor large integers and solve discrete logarithm problems in polynomial time. Every widely deployed asymmetric cryptosystem — RSA, ECC, DSA, DH — relies on one of those two problems being hard. On a sufficiently powerful quantum computer, none of them are.

**Grover's algorithm** provides a quadratic speedup for searching unstructured data, which effectively halves the security of symmetric ciphers and hash functions. AES-128 drops to ~64 bits of effective security. SHA-256 drops to ~128 bits of collision resistance.

CNSA 2.0 (2022) and NIST's finalized PQC standards (2024) define the approved replacements.

---

## CRITICAL — Broken by Shor's algorithm

These algorithms provide **no meaningful security** against a cryptographically relevant quantum computer. CNSA 2.0 requires migration away from all of them.

### RSA

| Field | Value |
|---|---|
| Risk | CRITICAL |
| Threat | Shor's algorithm factors the RSA modulus in polynomial time |
| Affects | All key sizes, including 4096-bit |
| NIST replacement (KEM) | ML-KEM — FIPS 203 (formerly CRYSTALS-Kyber) |
| NIST replacement (signatures) | ML-DSA — FIPS 204 (formerly CRYSTALS-Dilithium) |
| CNSA 2.0 deadline | 2030 (sooner for new systems) |

**What Qorex flags:** `RSA`, `rsa.generate_private_key`, `RSA_generate_key`, `RSA_new`, `crypto/rsa`, `KeyPairGenerator.getInstance("RSA")`

---

### ECDH

| Field | Value |
|---|---|
| Risk | CRITICAL |
| Threat | Shor's algorithm solves the elliptic curve discrete logarithm |
| Affects | All named curves: P-256, P-384, P-521, Curve25519 |
| NIST replacement | ML-KEM — FIPS 203 |
| CNSA 2.0 deadline | 2030 |

**What Qorex flags:** `ECDH`, `ec.ECDH`, `ECDH_compute_key`, `elliptic.P-256`, `elliptic.P-384`, `ecdh.GenerateKey`

---

### ECDSA

| Field | Value |
|---|---|
| Risk | CRITICAL |
| Threat | Shor's algorithm solves the elliptic curve discrete logarithm |
| Affects | All named curves |
| NIST replacement | ML-DSA — FIPS 204, or SLH-DSA — FIPS 205 (formerly SPHINCS+) |
| CNSA 2.0 deadline | 2030 |

**What Qorex flags:** `ECDSA`, `ec.ECDSA`, `ECDSA_sign`, `ecdsa.Sign`, `crypto/ecdsa`, `Signature.getInstance("SHA*withECDSA")`

---

### DSA

| Field | Value |
|---|---|
| Risk | CRITICAL |
| Threat | Shor's algorithm solves the discrete logarithm problem |
| Affects | All parameter sizes |
| NIST replacement | ML-DSA — FIPS 204 |
| CNSA 2.0 deadline | Already disallowed under CNSA 1.0 |

**What Qorex flags:** `DSA`, `dsa.generate_parameters`, `dsa.generate_private_key`, `DSA_generate_key`, `DSA_new`, `crypto/dsa`, `KeyPairGenerator.getInstance("DSA")`

---

### DH / DHE

| Field | Value |
|---|---|
| Risk | CRITICAL |
| Threat | Shor's algorithm solves the discrete logarithm problem |
| Affects | All group sizes; also applies to TLS DHE cipher suites |
| NIST replacement | ML-KEM — FIPS 203 |
| CNSA 2.0 deadline | 2030 |

**What Qorex flags:** `Diffie-Hellman`, `DiffieHellman`, `dh.generate_parameters`, `DH_generate_key`, `DH_new`, `crypto/dh`, `KeyAgreement.getInstance("DH")`, `DHE`, `_DHE_`

---

## HIGH — Weakened by Grover's algorithm

These algorithms are not broken outright, but Grover's algorithm provides a quadratic speedup that effectively halves their security level. They remain usable at larger key or output sizes.

### AES-128

| Field | Value |
|---|---|
| Risk | HIGH |
| Threat | Grover's algorithm reduces effective security to ~64 bits |
| Affects | AES-128 only; AES-256 is approved |
| CNSA 2.0 requirement | AES-256 |

**What Qorex flags:** `AES-128`, `AES128`, `EVP_aes_128_*`, patterns indicating 128-bit AES usage

**Note:** Some patterns (e.g. `algorithms.AES`, `AES.new()`, `aes.NewCipher()`) flag the call site regardless of key length, because key length is typically determined at runtime. Verify the actual key size at the flagged location.

---

### SHA-256

| Field | Value |
|---|---|
| Risk | HIGH |
| Threat | Grover's algorithm reduces collision resistance to ~128 bits |
| Affects | SHA-256 and SHA-224; SHA-384 and SHA-512 are approved |
| CNSA 2.0 requirement | SHA-384 or SHA-512 |

**What Qorex flags:** `SHA-256`, `SHA256`, `hashlib.sha256`, `SHA256_Init`, `SHA256_Update`, `sha256.New()`, `MessageDigest.getInstance("SHA-256")`

---

## Risk levels at a glance

| Level | Meaning | Action |
|---|---|---|
| CRITICAL | Algorithm provides no meaningful quantum security | Migrate before 2030; prioritize for new systems now |
| HIGH | Algorithm is weakened, not broken | Upgrade to larger variant (AES-256, SHA-384+) |

---

## NIST PQC standards reference

| Standard | Algorithm | Use case |
|---|---|---|
| FIPS 203 | ML-KEM (CRYSTALS-Kyber) | Key encapsulation / key exchange |
| FIPS 204 | ML-DSA (CRYSTALS-Dilithium) | Digital signatures |
| FIPS 205 | SLH-DSA (SPHINCS+) | Digital signatures (stateless hash-based) |
