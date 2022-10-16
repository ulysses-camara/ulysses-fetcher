"""Check integrity of downloaded resource."""
import typing as t
import hashlib


def check_resource_hash(
    resource_uri: str,
    resource_hash: str,
    read_block_size_in_mib: int = 256,
    hash_fn: t.Callable[[], t.Any] = hashlib.sha256,
) -> bool:
    """Check whether a downloaded file has the expected hash value.

    Parameters
    ----------
    resource_uri : str
        File URI to compute hash from.

    resource_hash : str
        Expected hash value.

    read_block_size_in_mib : int, default=128
        Size of blocks to read `resource_uri` file, in MebiBytes (MiB).

    hash_fn : t.Callable[[], t.Any], default=hashlib.sha256
        Hash function to compute, from hashlib.

    Returns
    -------
    hash_does_match : bool
        True if resource hash from `resource_uri` matches provided `resource_hash`.

    See Also
    --------
    hashlib : Python's native package to compute hashes.
    """
    hasher = hash_fn()

    read_block_size_in_b = 1024 * 1024 * read_block_size_in_mib

    with open(resource_uri, "rb") as f_in:
        for data_chunk in iter(lambda: f_in.read(read_block_size_in_b), b""):
            hasher.update(data_chunk)

    return bool(hasher.hexdigest() == resource_hash)
