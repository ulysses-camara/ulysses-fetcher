"""Check integrity of downloaded model."""
import typing as t
import hashlib


def check_model_hash(
    model_uri: str,
    model_hash: str,
    read_block_size: int = 65536,
    hash_fn: t.Callable[[], t.Any] = hashlib.sha256,
) -> bool:
    """Check whether a downloaded file has the expected hash value."""
    hasher = hash_fn()

    with open(model_uri, "rb") as f_in:
        for data_chunk in iter(lambda: f_in.read(read_block_size), b""):
            hasher.update(data_chunk)

    return bool(hasher.hexdigest() == model_hash)
