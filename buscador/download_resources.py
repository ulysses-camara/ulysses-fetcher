"""Retrieve resources for the Ulysses project."""
import typing as t
import urllib.request
import os
import json
import warnings
import socket
import contextlib
import glob
import shutil

import tqdm

from . import integrity
from . import decompress


__all__ = [
    "download_resource",
    "get_available_tasks",
    "get_task_available_resources",
    "DEFAULT_URIS",
    "DEFAULT_URIS_CONFIG_DIR",
]


DEFAULT_URIS: t.Dict[str, t.Any] = {}
DEFAULT_URIS_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "trusted_urls")

try:
    for config_file_uri in glob.glob(os.path.join(DEFAULT_URIS_CONFIG_DIR, "*.json")):
        with open(config_file_uri, "r", encoding="utf-8") as f_config:
            new_config = json.load(f_config)

        for key, value in new_config.items():
            if key in DEFAULT_URIS:
                DEFAULT_URIS[key].update(value)
            else:
                DEFAULT_URIS[key] = value


except (OSError, FileNotFoundError):
    DEFAULT_URIS = {}
    warnings.warn(
        message=(
            f"Could not open '{DEFAULT_URIS_CONFIG_DIR}', hence this package will be unable "
            "to retrieve resource URLs."
        ),
        category=RuntimeWarning,
    )


class ResourceHashError(Exception):
    """Error raises when downloaded resource hash does not match expected hash value."""


@contextlib.contextmanager
def _set_connection_timeout(timeout_in_seconds: int) -> t.Iterator[None]:
    """Set connection timeout (in seconds) for stale downloads."""
    def_timeout = socket.getdefaulttimeout()

    try:
        socket.setdefaulttimeout(timeout_in_seconds)
        yield None

    finally:
        socket.setdefaulttimeout(def_timeout)


def download_file(
    url: str,
    output_uri: str,
    show_progress_bar: bool = True,
    check_cached: bool = True,
    timeout_limit_seconds: int = 10,
) -> None:
    """Download a file from the provided `url`.

    Parameters
    ----------
    url : str
        URL to download file from.

    output_uri : str
        Output URI (full path, ending with the filename and its extension) to save file.

    show_progress_bar: bool, default=True
        If True, show download progress bar.

    check_cached : bool, default=True
        If True, do not download file if a file with the same `output_uri` exists locally.

    timeout_limit_seconds : int, default=10
        Timeout limit for stale downloads, in seconds.

    Returns
    -------
    None
    """
    if check_cached and os.path.isfile(output_uri):
        return

    pbar = None

    def fn_progress_bar(block_num: int, block_size: int, total_size: int) -> None:
        # pylint: disable='unused-argument'
        nonlocal pbar

        if pbar is None:
            _, filename = os.path.split(output_uri)
            pbar = tqdm.tqdm(
                total=total_size,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
                desc=f"Downloading {filename}",
            )

        pbar.update(block_size)

    try:
        with _set_connection_timeout(timeout_in_seconds=timeout_limit_seconds):
            urllib.request.urlretrieve(
                url=url,
                filename=output_uri,
                reporthook=fn_progress_bar if show_progress_bar else None,
            )

    except Exception as err:
        if os.path.isfile(output_uri):
            os.remove(output_uri)

        raise ConnectionError(f"Could not download resource from '{output_uri}'.") from err

    except KeyboardInterrupt as kbi_err:
        if os.path.isfile(output_uri):
            os.remove(output_uri)

        raise KeyboardInterrupt from kbi_err

    return


def download_resource_from_url(
    resource_url: str,
    output_uri: str,
    show_progress_bar: bool = True,
    check_cached: bool = True,
    clean_compressed_files: bool = True,
    expected_resource_hash: t.Optional[str] = None,
    timeout_limit_seconds: int = 10,
) -> None:
    """Download a resource from the provided `url`.

    Zipped files are decompressed.

    Parameters
    ----------
    resource_url : str
        URL to download resource from.

    output_uri : str
        Output URI (full path, ending with the filename and its extension) to save resource.

    show_progress_bar: bool, default=True
        If True, show download progress bar.

    check_cached : bool, default=True
        If True, do not download file if a file with the same `output_uri` exists locally.

    clean_compressed_files : bool, default=True
        If True, delete compressed files after decompression.

    expected_resource_hash : str or None, default=None
        Check whether downloaded resource hash matches the provided value.

    timeout_limit_seconds : int, default=10
        Timeout limit for stale downloads, in seconds.

    Returns
    -------
    None
    """
    if check_cached:
        output_uri_noext = ".".join(output_uri.split(".")[:-1])

        output_file_is_cached = any(
            not (filename.endswith(".zip") or filename.endswith(".tar"))
            for filename in glob.glob(f"{output_uri_noext}*")
        )
        if os.path.isdir(output_uri_noext) or output_file_is_cached:
            return

    download_file(
        url=resource_url,
        output_uri=output_uri,
        show_progress_bar=show_progress_bar,
        check_cached=check_cached,
        timeout_limit_seconds=timeout_limit_seconds,
    )

    hash_has_issues = expected_resource_hash is not None and not integrity.check_resource_hash(
        resource_uri=output_uri, resource_hash=expected_resource_hash
    )

    if hash_has_issues:
        if os.path.isfile(output_uri):
            os.remove(output_uri)

        if os.path.isdir(output_uri):
            shutil.rmtree(output_uri)

        raise ResourceHashError

    decompress.decompress(output_uri, clean_compressed_files=clean_compressed_files)


def download_resource(
    task_name: str,
    resource_name: str,
    output_dir: str = ".",
    show_progress_bar: bool = True,
    check_cached: bool = True,
    clean_compressed_files: bool = True,
    check_resource_hash: bool = True,
    timeout_limit_seconds: int = 10,
) -> bool:
    """Download a resource from the provided (`task_name`, `resource_name`) pair.

    Both `task_name` and `resource_name` must be properly configured in ``trusted_urls`` directory.

    Parameters
    ----------
    task_name : str
        Resource task name. Call ``buscador.get_available_tasks()`` for a complete task list.

    resource_name : str
        Resource name to download. Call ``buscador.get_task_available_resources(task_name)``
        for a complete resource list for a specific ``task_name``.

    output_dir : str
        Directory to save the downloaded resource.

    show_progress_bar: bool, default=True
        If True, show download progress bar.

    check_cached : bool, default=True
        If True, do not download file if a file with the same `output_uri` exists locally.

    clean_compressed_files : bool, default=True
        If True, delete compressed files after decompression.

    check_resource_hash : bool, default=True
        If True, verify if the downloaded resource hash (SHA256) matches the correct value.

    timeout_limit_seconds : int, default=10
        Timeout limit for stale downloads, in seconds.

    Returns
    -------
    was_succeed : bool
        True if file was downloaded successfully (or found locally when `check_cached=True`).
    """
    ResourceConfigType = t.Dict[str, t.Any]

    try:
        resource_map: t.Dict[str, ResourceConfigType] = DEFAULT_URIS[task_name]

    except KeyError as k_err:
        valid_tasks = ", ".join(map("'{}'".format, sorted(DEFAULT_URIS.keys())))

        raise ValueError(
            f"Unknown task '{task_name}'. Please provide one of the following: "
            f"{valid_tasks}."
        ) from k_err

    try:
        resource_config: ResourceConfigType = resource_map[resource_name]

    except KeyError as k_err:
        valid_resources = ", ".join(map("'{}'".format, sorted(resource_map.keys())))

        raise ValueError(
            f"Unknown resource '{resource_name}' for task '{task_name}'. Please verify if the "
            f"provided task is correct ('{task_name}'). If that is the case, plase provide one of "
            f"the following resources: {valid_resources}."
        ) from k_err

    output_dir = output_dir.strip()
    output_dir = os.path.expanduser(output_dir)
    output_dir = os.path.expandvars(output_dir)
    output_dir = os.path.realpath(output_dir)

    os.makedirs(output_dir, exist_ok=True)

    resource_sha256 = resource_config["sha256"]
    f_extension = resource_config["file_extension"]

    for resource_url in resource_config["urls"]:
        output_uri = os.path.join(output_dir, f"{resource_name}{f_extension}").strip()
        resource_url = resource_url.strip()

        try:
            download_resource_from_url(
                resource_url=resource_url,
                output_uri=output_uri,
                show_progress_bar=show_progress_bar,
                check_cached=check_cached,
                clean_compressed_files=clean_compressed_files,
                expected_resource_hash=resource_sha256 if check_resource_hash else None,
                timeout_limit_seconds=timeout_limit_seconds,
            )

        except (ConnectionError, urllib.error.URLError) as conn_err:
            warnings.warn(
                message=(
                    f"Could not retrieve '{resource_name}' for '{task_name}' task in "
                    f"'{resource_url}' address (error message: {conn_err})."
                ),
                category=RuntimeWarning,
            )
            continue

        except ResourceHashError:
            warnings.warn(
                message=f"Unmatched resource hash (SHA256) from URL '{resource_url}'. Skipping it.",
                category=RuntimeWarning,
            )
            continue

        return True

    try:
        os.rmdir(output_dir)

    except OSError:
        pass

    return False


def get_available_tasks() -> t.Tuple[str, ...]:
    """Get all available tasks to get resources from."""
    return tuple(DEFAULT_URIS.keys())


def get_task_available_resources(task_name: str) -> t.Tuple[str, ...]:
    """Get all available resources from the provided task.

    See also
    --------
    get_available_tasks : get all available tasks.
    """
    if task_name not in DEFAULT_URIS:
        valid_tasks = ", ".join(get_available_tasks())
        raise ValueError(
            f"Unrecognized task name '{task_name}'. Please provide one of the following: "
            f"{valid_tasks}."
        )

    return tuple(DEFAULT_URIS[task_name].keys())
