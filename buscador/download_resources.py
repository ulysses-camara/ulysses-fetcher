"""Retrieve resources for the Ulysses project."""
import typing as t
import os
import json
import warnings
import glob
import shutil

import gdown

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
    """Raised when downloaded resource hash does not match expected hash value."""


def _is_resource_cached(output_uri: str) -> bool:
    """
    Check whether a resource (or its decompressed contents) already exists.
    """
    output_uri_noext = os.path.splitext(output_uri)[0]

    if os.path.isdir(output_uri_noext):
        return True

    for filename in glob.glob(f"{output_uri_noext}*"):
        if not filename.endswith((".zip", ".tar")):
            return True

    return False


def _download_file(
    url: str,
    output_uri: str,
    show_progress_bar: bool,
    check_cached: bool,
) -> None:
    """
    Download a file from Google Drive using gdown.
    """
    if check_cached and os.path.isfile(output_uri):
        return

    try:
        gdown.download(
            url=url,
            output=output_uri,
            quiet=not show_progress_bar,
            fuzzy=True,
        )

    except Exception as err:
        if os.path.isfile(output_uri):
            os.remove(output_uri)
        raise ConnectionError(f"Could not download resource from '{url}'. Error message: {err}") from err


def _download_resource_from_url(
    resource_url: str,
    output_uri: str,
    show_progress_bar: bool,
    check_cached: bool,
    clean_compressed_files: bool,
    expected_resource_hash: t.Optional[str],
) -> None:
    """
    Download, validate, and decompress a resource from a single URL.
    """
    if check_cached and _is_resource_cached(output_uri):
        return

    _download_file(
        url=resource_url,
        output_uri=output_uri,
        show_progress_bar=show_progress_bar,
        check_cached=check_cached,
    )

    if expected_resource_hash is not None:
        if not integrity.check_resource_hash(
            resource_uri=output_uri,
            resource_hash=expected_resource_hash,
        ):
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
    timeout_limit_seconds: int = 10,  # kept for backward compatibility
) -> bool:
    """Download a resource from the provided (`task_name`, `resource_name`) pair."""
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
            f"provided task is correct ('{task_name}'). If that is the case, please provide one of "
            f"the following resources: {valid_resources}."
        ) from k_err

    output_dir = os.path.realpath(
        os.path.expandvars(os.path.expanduser(output_dir.strip()))
    )
    os.makedirs(output_dir, exist_ok=True)

    resource_sha256 = resource_config["sha256"]
    file_extension = resource_config["file_extension"]

    for resource_url in resource_config["urls"]:
        output_uri = os.path.join(output_dir, f"{resource_name}{file_extension}")

        try:
            _download_resource_from_url(
                resource_url=resource_url.strip(),
                output_uri=output_uri,
                show_progress_bar=show_progress_bar,
                check_cached=check_cached,
                clean_compressed_files=clean_compressed_files,
                expected_resource_hash=resource_sha256 if check_resource_hash else None,
            )

        except ConnectionError as conn_err:
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
    """Get all available resources from the provided task."""
    if task_name not in DEFAULT_URIS:
        valid_tasks = ", ".join(get_available_tasks())
        raise ValueError(
            f"Unrecognized task name '{task_name}'. Please provide one of the following: "
            f"{valid_tasks}."
        )

    return tuple(DEFAULT_URIS[task_name].keys())
