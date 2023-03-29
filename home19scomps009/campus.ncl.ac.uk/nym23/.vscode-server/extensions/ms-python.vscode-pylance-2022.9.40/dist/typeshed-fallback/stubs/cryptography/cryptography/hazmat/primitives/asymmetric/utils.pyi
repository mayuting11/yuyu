from cryptography.hazmat.primitives.hashes import HashAlgorithm

def decode_dss_signature(signature: bytes) -> tuple[int, int]: ...
def encode_dss_signature(r: int, s: int) -> bytes: ...

class Prehashed:
    _algorithm: HashAlgorithm  # undocumented
    _digest_size: int  # undocumented
    def __init__(self, algorithm: HashAlgorithm) -> None: ...
    @property
    def digest_size(self) -> int: ...
