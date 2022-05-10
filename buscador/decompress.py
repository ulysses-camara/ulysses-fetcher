"""Decompress compressed files."""
import typing as t
import re
import os

import zipfile
import tarfile


COMPRESSION_ALG: t.Dict[str, t.Type[t.Any]] = {
    "zip": zipfile.ZipFile,
    "tar": tarfile.TarFile,
}

RE_GET_EXT = re.compile(r"\.(.*)$")


def decompress(output_uri: str, clean_zip_files: bool = False) -> None:
    """Decompress a compressed file."""
    match_file_ext = RE_GET_EXT.search(output_uri)

    if not match_file_ext:
        return

    file_ext = match_file_ext.group(1)

    if file_ext not in COMPRESSION_ALG:
        return

    output_dir, _ = os.path.split(output_uri)
    fn_compressed_file = COMPRESSION_ALG[file_ext]

    with fn_compressed_file(output_uri) as f_compressed:
        f_compressed.extractall(path=output_dir)

    if clean_zip_files:
        os.remove(output_uri)
