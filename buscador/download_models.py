"""Retrieve pretrained models for the Ulysses project."""
import typing as t
import urllib.request
import os
import json
import zipfile
import warnings
import socket
import contextlib
import glob

import tqdm


__all__ = [
    "download_model",
]


DEFAULT_URIS: t.Dict[str, t.Any]
DEFAULT_URIS_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "default_uris.json")

try:
    with open(DEFAULT_URIS_CONFIG_FILE, "r", encoding="utf-8") as f_config:
        DEFAULT_URIS = json.load(f_config)

except (OSError, FileNotFoundError):
    DEFAULT_URIS = {}
    warnings.warn(
        message=(
            f"Could not open '{DEFAULT_URIS_CONFIG_FILE}', hence this package will be unable "
            "to retrieve pretrained model URLs."
        ),
        category=RuntimeWarning,
    )


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
) -> None:
    """Download a file from the provided `url`.

    Parameters
    ----------
    url : str
        URL to donwload file from.

    output_uri : str
        Output URI (full path, ending with the filename and its extension) to save file.

    show_progress_bar: bool, default=True
        If True, show download progress bar.

    check_cached : bool, default=True
        If True, do not download file if a file with the same `output_uri` exists locally.

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
            _, filename = os.path.split(url)
            pbar = tqdm.tqdm(
                total=total_size,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
                desc=f"Downloading {filename}",
            )

        pbar.update(block_size)

    try:
        with _set_connection_timeout(timeout_in_seconds=5):
            urllib.request.urlretrieve(
                url=url,
                filename=output_uri,
                reporthook=fn_progress_bar if show_progress_bar else None,
            )

    except Exception as err:
        os.remove(output_uri)
        raise ConnectionError(f"Could not download pretrained model from '{output_uri}'.") from err

    except KeyboardInterrupt as kbi_err:
        os.remove(output_uri)
        raise KeyboardInterrupt from kbi_err

    return


def download_model_from_url(
    model_url: str,
    output_uri: str,
    show_progress_bar: bool = True,
    check_cached: bool = True,
    clean_zip_files: bool = True,
) -> None:
    """Download a pretrained model from the provided `url`.

    Zipped files are decompressed.

    Parameters
    ----------
    model_url : str
        URL to donwload pretrained model from.

    output_uri : str
        Output URI (full path, ending with the filename and its extension) to save model.

    show_progress_bar: bool, default=True
        If True, show download progress bar.

    check_cached : bool, default=True
        If True, do not download file if a file with the same `output_uri` exists locally.

    clean_zip_files : bool, default=True
        If True, delete zip files after decompression.

    Returns
    -------
    None
    """
    output_uri_noext = ".".join(output_uri.split(".")[:-1])

    output_file_is_cached = any(
        True for filename in glob.glob(f"{output_uri_noext}.*") if not filename.endswith(".zip")
    )
    if os.path.isdir(output_uri_noext) or output_file_is_cached:
        return

    download_file(
        url=model_url,
        output_uri=output_uri,
        show_progress_bar=show_progress_bar,
        check_cached=check_cached,
    )

    if not output_uri.endswith(".zip"):
        return

    with zipfile.ZipFile(output_uri) as zipf:
        zipf.extractall()

    if clean_zip_files:
        os.remove(output_uri)


def download_model(
    task_name: str,
    model_name: str,
    output_dir: str = ".",
    show_progress_bar: bool = True,
    check_cached: bool = True,
    clean_zip_files: bool = True,
) -> bool:
    """Download a pretrained model from the provided (`task_name`, `model_name`) pair.

    Both `task_name` and `model_name` must be properly configured in ``default_uris.json``.

    Parameters
    ----------
    task_name : str
        Model task name.

    model_name : str
        Model name to download.

    output_dir : str
        Directory to save the downloaded model.

    show_progress_bar: bool, default=True
        If True, show download progress bar.

    check_cached : bool, default=True
        If True, do not download file if a file with the same `output_uri` exists locally.

    clean_zip_files : bool, default=True
        If True, delete zip files after decompression.

    Returns
    -------
    was_succeed : bool
        True if file was downloaded successfully (or found locally when `check_cached=True`).
    """
    try:
        model_map: t.Dict[str, t.Union[t.Sequence[str], str]] = DEFAULT_URIS[task_name]

    except KeyError as k_err:
        valid_tasks = ", ".join(sorted(DEFAULT_URIS.keys()))

        raise ValueError(
            f"Unsupported task '{task_name}'. Plase provide one of the following: "
            f"{valid_tasks}."
        ) from k_err

    try:
        model_urls: t.Union[t.Sequence[str], str] = model_map[model_name]

    except KeyError as k_err:
        valid_models = ", ".join(sorted(model_map.keys()))

        raise ValueError(
            f"Unknown model '{model_name}' for task '{task_name}'. Please verify is the provided "
            f"task is correct and, if so, provide one of the following models: {valid_models}."
        ) from k_err

    if isinstance(model_urls, str):
        model_urls = [model_urls]

    for model_url in model_urls:
        _, filename = os.path.split(model_url)
        output_uri = os.path.join(output_dir, filename)

        try:
            download_model_from_url(
                model_url=model_url,
                output_uri=output_uri,
                show_progress_bar=show_progress_bar,
                check_cached=check_cached,
                clean_zip_files=clean_zip_files,
            )
            return True

        except (ConnectionError, urllib.error.URLError) as conn_err:
            warnings.warn(
                message=(
                    f"Could not retrieve '{model_name}' for '{task_name}' task in "
                    f"'{model_url}' address (error message: {conn_err})."
                ),
                category=RuntimeWarning,
            )

    return False


def get_avaliable_tasks() -> t.Tuple[str, ...]:
    """Get all available tasks to get pretrained models from."""
    return tuple(DEFAULT_URIS.keys())


def get_task_avaliable_models(task_name: str) -> t.Tuple[str, ...]:
    """Get all available models from the provided task.

    See also
    --------
    get_avaliable_tasks : get all available tasks.
    """
    if task_name not in DEFAULT_URIS:
        valid_tasks = ", ".join(get_available_tasks())
        raise ValueError(
            f"Unrecognized task name '{task_name}'. Please provide one of the following: "
            f"{valid_tasks}."
        )

    return tuple(DEFAULT_URIS[task_name].keys())
