# Ulysses Fetcher
Fetch pretrained models for Ulysses project.

---

## Table of contents
1. [Installation](#installation)
2. [Usage as package](#usage-as-package)
3. [Usage by command line](#usage-by-command-line)
4. [License](#license)

---

## Instalation
```bash
python -m pip install "git+https://github.com/ulysses-camara/ulysses-fetcher"
```
---

## Usage as package

```python
import buscador

has_succeed = buscador.download_model(
    task_name="<task_name>",
    model_name="<model_name_given_the_task>",
    output_dir="<directory_to_save_downloaded_models>",
    show_progress_bar=True,
    check_cached=True,
    clean_zip_files=True,
    check_model_hash=True,
    timeout_limit_seconds=10,
)

print("Download was sucessfull!" if has_succeed "Download was not sucessfull.")
```

- **task_name** (*str*): Model task name. You can get a list of curretnyl supported tasks programatically by using `buscador.get_available_tasks()`. The list of supported tasks are:
  - **legal_text_segmentation**: Segmentation of Brazilian Legal texts.
- **model_name** (*str*): Model to be downloaded. You can get a list of available models per task by using `buscador.get_task_available_models(task_name)`.
- **output_dir** (*str*): Output directory to save downloaded models.
- **show_progress_bar** (*bool*): If True, display progress bar.
- **check_cached** (*bool*): If True, do not download models if a file with the same output URI is found.
- **clean_zip_files** (*bool*): If True, remove `.zip` files after decompression.
- **check_model_hash** (*bool*): If True, verify if downloaded file hash matches the expected hash value.
- **timeout_limit_seconds** (*int*): Maximum number of seconds to cancel staled downloads.

---

## Usage by command line
This package can be used directly from command line as module after installation:
```bash
python -m buscador --help
```
- Positional arguments:
  - `task_name`: Task name to retrieve a pretrained model from. Must be one of the following: legal_text_segmentation.
  - `model_name`: Pretrained model name to retrieve.

- Optional arguments:
  - `-h`, `--help`: display help message.
  - `--output-dir`: Output directory to store downloaded models.
  - `--timeout-limit TIMEOUT_LIMIT`: Timeout limit for stale downloads, in seconds.
  - `--disable-progress-bar`: If enabled, do not display progress bar.
  - `--ignore-cached-files`: If enabled, download files even they are found locally.
  - `--keep-zip-files`: If enabled, do not exclude `.zip` files after decompression.
  - `--ignore-model-hash`: If enabled, do not verify downloaded file hash.

---

## License
[MIT.](./LICENSE)
