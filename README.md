# Ulysses Fetcher
Fetch pretrained models for Ulysses project.

---

## Table of contents
1. [Installation](#installation)
2. [Usage as package](#usage-as-package)
3. [Usage by command line](#usage-by-command-line)
4. [For developers](#for-developers)
    1. [Register a new pretrained model](#register-a-new-pretrained-model)
5. [License](#license)

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
    clean_compressed_files=True,
    check_model_hash=True,
    timeout_limit_seconds=10,
)

print("Download was successfull!" if has_succeed else "Download was not successfull.")
```

- **task_name** (*str*): Model task name. You can get a list of currently supported tasks programatically by using `buscador.get_available_tasks()`. The list of supported tasks are:
  - **legal_text_segmentation**: Segmentation of Brazilian Legal texts.
- **model_name** (*str*): Model to download. You can get a list of available models per task by using `buscador.get_task_available_models(task_name)`.
- **output_dir** (*str*): Output directory to save downloaded models.
- **show_progress_bar** (*bool, default=True*): If True, display progress bar.
- **check_cached** (*bool, default=True*): If True, do not download models if a file with the same output URI is found.
- **clean_compressed_files** (*bool, default=True*): If True, remove compressed files after decompression.
- **check_model_hash** (*bool, default=True*): If True, verify if downloaded file hash matches the expected hash value.
- **timeout_limit_seconds** (*int, default=10*): Number of seconds until abortion of staled downloads.

---

## Usage by command line
This package can be used directly from command line as module after installation:
```bash
python -m buscador --help
```
- Positional arguments:
  - `task_name`: Task name to retrieve a pretrained model from.
  - `model_name`: Pretrained model name to retrieve.

- Optional arguments:
  - `-h`, `--help`: display help message.
  - `--output-dir`: Output directory to store downloaded models.
  - `--timeout-limit TIMEOUT_LIMIT`: Timeout limit for stale downloads, in seconds.
  - `--disable-progress-bar`: If enabled, do not display progress bar.
  - `--ignore-cached-files`: If enabled, download files even they are found locally.
  - `--keep-compressed-files`: If enabled, do not exclude `.zip` files after decompression.
  - `--ignore-model-hash`: If enabled, do not verify if downloaded file hash matches the expected value.

---

## For developers

### Register a new pretrained model
To register a new pretrained model in Ulysses Fetcher, please follow the steps below:
1. Compress your pretrained model as either `.zip` or `.tar` format (if it is a PyTorch binary, `.pt`, you can skip this step).
2. Store your pretrained model in a couple of cloud storage services, and get their directly download URL. It is recommended to store your model in at least two distinct cloud providers.
3. Hash you pretrained model by using SHA256 from Python hashlib, as follows:
```python
import hashlib

read_block_size_in_bytes = 64 * 1024 * 1024  # Read file in blocks of 64MiB; or any other amount.
hasher = hashlib.sha256()

with open("path_to_my_compressed_pretrained_model", "rb") as f_in:
    for data_chunk in iter(lambda: f_in.read(read_block_size_in_bytes), b""):
        hasher.update(data_chunk)

my_model_sha256 = hasher.hexdigest()
print(my_model_sha256)
```
4. Edit the [default_uris.json](./buscador/default_uris.json) file, providing the model task, model name, file extension (`.zip` or `.tar` for compressed models), its computed SHA256, and the direct download URLs as depicted in the exemple below. Note that Ulysses Fetcher will try to download models by following the provided order in `urls`. Hence, later URLs are fallback addresses in case something went wrong with every previous URL.
```json
{
  "model_task": {
    "sha256": "<my_model_sha256>",
    "file_extension": ".zip",
    "urls": [
      "https://url_1",
      "https://url_2",
      ...
    ]
  }
}
```
5. Create a Pull Request with your changes, providing all information about your model. Your contribution will be reviewed and, if appropriate to this package, it may get accepted.

---

## License
[MIT.](./LICENSE)
