"""Check integrity of downloaded model."""
import typing as t
import hashlib


def check_model_hash(
    model_uri: str,
    model_hash: str,
    read_block_size_in_mib: int = 256,
    hash_fn: t.Callable[[], t.Any] = hashlib.sha256,
) -> bool:
    """Check whether a downloaded file has the expected hash value.

    Parameters
    ----------
    model_uri : str
        File URI to compute hash from.

    model_hash : str
        Expected hash value.

    read_block_size_in_mib : int, default=128
        Size of blocks to read `model_uri` file, in MebiBytes (MiB).

    hash_fn : t.Callable[[], t.Any], default=hashlib.sha256
        Hash function to compute, from hashlib.

    Returns
    -------
    hash_does_match : bool
        True if model hash from `model_uri` matches provided `model_hash`.

    See Also
    --------
    hashlib : Python's native package to compute hashes.
    """
    hasher = hash_fn()

    read_block_size_in_b = 1024 * 1024 * read_block_size_in_mib

    with open(model_uri, "rb") as f_in:
        for data_chunk in iter(lambda: f_in.read(read_block_size_in_b), b""):
            hasher.update(data_chunk)

    return bool(hasher.hexdigest() == model_hash)
