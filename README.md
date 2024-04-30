[![Tests](https://github.com/ulysses-camara/ulysses-fetcher/actions/workflows/tests.yml/badge.svg)](https://github.com/ulysses-camara/ulysses-fetcher/actions/workflows/tests.yml)

# Ulysses Fetcher
Fetch resources for Ulysses project.

---

## Table of Contents
1. [Installation](#installation)
2. [Available resources](#available-resources)
    1. [Pretrained machine learning models](#pretrained-machine-learning-models)
    2. [Datasets](#datasets)
    3. [Deprecated resources](#deprecated-resources)
3. [Usage (as a library)](#usage-as-a-library)
4. [Usage by command line](#usage-by-command-line)
5. [For developers](#for-developers)
    1. [Register a new resource](#register-a-new-resource)
6. [License](#license)

---

## Instalation
```bash
python -m pip install "git+https://github.com/ulysses-camara/ulysses-fetcher"
```
---

## Available resources

### Pretrained machine learning models

| Task name | Model name |
| --------- | ---------- |
| `legal_text_segmentation` | - `2_layer_6000_vocab_size_bert_v3` <br> - `4_layer_6000_vocab_size_bert_v3` <br> - `256_hidden_dim_6000_vocab_size_1_layer_lstm_v3`<br> - `6000_subword_tokenizer`|
| `sentence_similarity`     | - `legal_sroberta_v0` <br> - `legal_sroberta_v1` <br> - `sbert_1mil_anama` <br> - `sbert_650k_nheeng` <br> - `sbert_map2doc_v1` <br> - `ulysses_LaBSE_3000` |

### Datasets



| Task name | Dataset name |
| --------- | ---------- |
| `sentence_model_evaluation` | - `bill_summary_to_topics` <br> - `code_estatutes_cf88` <br> - `factnews_news_bias` <br> - `factnews_news_factuality` <br> - `fakebr_size_normalized` <br> - `faqs` <br> - `hatebr_offensive_lang` <br> - `masked_law_name_in_news` <br> - `masked_law_name_in_summaries` <br> - `oab_first_part` <br> - `oab_second_part` <br> - `offcombr2` <br> - `stj_summary` <br> - `sts_state_news` <br> - `summary_vs_bill` <br> - `tampered_leg` <br> - `trf_examinations` <br> - `ulysses_sd` |
| `probing_task`     | - `dataset_wikipedia_ptbr_bigram_shift_v1` <br> - `dataset_wikipedia_ptbr_coordination_inversion_v1` <br> - `dataset_wikipedia_ptbr_obj_number_v1` <br> - `dataset_wikipedia_ptbr_odd_man_out_v1` <br> - `dataset_wikipedia_ptbr_past_present_v1` <br> - `dataset_wikipedia_ptbr_sentence_length_v1` <br> - `dataset_wikipedia_ptbr_subj_number_v1` <br> - `dataset_wikipedia_ptbr_top_constituents_v1` <br> - `dataset_wikipedia_ptbr_tree_depth_v1` <br> - `dataset_wikipedia_ptbr_word_content_v1` <br> - `dataset_sp_court_cases_bigram_shift_v1` <br> - `dataset_sp_court_cases_coordination_inversion_v1` <br> - `dataset_sp_court_cases_obj_number_v1` <br> - `dataset_sp_court_cases_odd_man_out_v1` <br> - `dataset_sp_court_cases_past_present_v1` <br> - `dataset_sp_court_cases_sentence_length_v1` <br> - `dataset_sp_court_cases_subj_number_v1` <br> - `dataset_sp_court_cases_top_constituents_v1` <br> - `dataset_sp_court_cases_tree_depth_v1` <br> - `dataset_sp_court_cases_word_content_v1` <br> - `dataset_political_speeches_ptbr_bigram_shift_v1` <br> - `dataset_political_speeches_ptbr_coordination_inversion_v1` <br> - `dataset_political_speeches_ptbr_obj_number_v1` <br> - `dataset_political_speeches_ptbr_odd_man_out_v1` <br> - `dataset_political_speeches_ptbr_past_present_v1` <br> - `dataset_political_speeches_ptbr_sentence_length_v1` <br> - `dataset_political_speeches_ptbr_subj_number_v1` <br> - `dataset_political_speeches_ptbr_top_constituents_v1` <br> - `dataset_political_speeches_ptbr_tree_depth_v1` <br> - `dataset_political_speeches_ptbr_word_content_v1` <br> - `dataset_leg_pop_comments_ptbr_bigram_shift_v1` <br> - `dataset_leg_pop_comments_ptbr_coordination_inversion_v1` <br> - `dataset_leg_pop_comments_ptbr_obj_number_v1` <br> - `dataset_leg_pop_comments_ptbr_odd_man_out_v1` <br> - `dataset_leg_pop_comments_ptbr_past_present_v1` <br> - `dataset_leg_pop_comments_ptbr_sentence_length_v1` <br> - `dataset_leg_pop_comments_ptbr_subj_number_v1` <br> - `dataset_leg_pop_comments_ptbr_top_constituents_v1` <br> - `dataset_leg_pop_comments_ptbr_tree_depth_v1` <br> - `dataset_leg_pop_comments_ptbr_word_content_v1` <br> - `dataset_leg_docs_ptbr_bigram_shift_v1` <br> - `dataset_leg_docs_ptbr_coordination_inversion_v1` <br> - `dataset_leg_docs_ptbr_obj_number_v1` <br> - `dataset_leg_docs_ptbr_odd_man_out_v1` <br> - `dataset_leg_docs_ptbr_past_present_v1` <br> - `dataset_leg_docs_ptbr_sentence_length_v1` <br> - `dataset_leg_docs_ptbr_subj_number_v1` <br> - `dataset_leg_docs_ptbr_top_constituents_v1` <br> - `dataset_leg_docs_ptbr_tree_depth_v1` <br> - `dataset_leg_docs_ptbr_word_content_v1` |
| `quantization` | - `ulysses_tesemo_v2_subset_static_quantization` |

### Deprecated resources

| Task name | Model name |
| --------- | ---------- |
| `legal_text_segmentation` | - ~~`2_layer_6000_vocab_size_bert_v2`~~ (DEPRECATED) <br> - ~~`4_layer_6000_vocab_size_bert_v2`~~ (DEPRECATED) <br> - ~~`256_hidden_dim_6000_vocab_size_1_layer_lstm_v2`~~ (DEPRECATED) <br> - ~~`2_layer_6000_vocab_size_bert`~~ (DEPRECATED) <br> - ~~`512_hidden_dim_6000_vocab_size_1_layer_lstm`~~ (DEPRECATED) |
| `sentence_similarity` | - ~~`distil_sbert_br_ctimproved_12_epochs_v1`~~ (DEPRECATED) |

---

## Usage (as a library)

```python
import buscador

has_succeed = buscador.download_resource(
    task_name="<task_name>",
    resource_name="<resource_name_given_the_task>",
    output_dir="<directory_to_save_downloaded_resources>",
    show_progress_bar=True,
    check_cached=True,
    clean_compressed_files=True,
    check_resource_hash=True,
    timeout_limit_seconds=10,
)

print("Download was successfull!" if has_succeed else "Download was not successfull.")
```

- **task_name** (*str*): Resource task name. You can get a list of currently supported tasks programatically by using `buscador.get_available_tasks()`;
- **resource_name** (*str*): Resource to download. You can get a list of available resources per task by using `buscador.get_task_available_resources(task_name)`;
- **output_dir** (*str*): Output directory to save downloaded resources;
- **show_progress_bar** (*bool, default=True*): If True, display progress bar;
- **check_cached** (*bool, default=True*): If True, do not download resources if a file with the same output URI is found;
- **clean_compressed_files** (*bool, default=True*): If True, remove compressed files after decompression;
- **check_resource_hash** (*bool, default=True*): If True, verify if downloaded file hash matches the expected hash value;
- **timeout_limit_seconds** (*int, default=10*): Limit in seconds until the abortion of staled downloads.

---

## Usage by command line
This library can be used directly from command line as module after installation:
```bash
python -m buscador --help
```
- Positional arguments:
  - `task_name`: Task name to retrieve a resource from.
  - `resource_name`: Pretrained resource name to retrieve.

- Optional arguments:
  - `-h`, `--help`: display help message.
  - `--output-dir`: Output directory to store downloaded resources.
  - `--timeout-limit TIMEOUT_LIMIT`: Timeout limit for stale downloads, in seconds.
  - `--disable-progress-bar`: If enabled, do not display progress bar.
  - `--ignore-cached-files`: If enabled, download files even they are found locally.
  - `--keep-compressed-files`: If enabled, do not exclude compressed files (`.zip`, `.tar`) after decompression.
  - `--ignore-resource-hash`: If enabled, do not verify if downloaded file hash matches the expected value.

---

## For developers

### Register a new resource
To register a new resource in Ulysses Fetcher, please follow the steps below:

1. Make sure that the resource filename (or directory name, in case your resource is represented by more than one file) matches **exactly** the desired resource name.

2. Compress your resource as either `.zip` or `.tar` format (if it is a PyTorch binary - `.pt` - you can skip this step).

```bash
zip -r my_resource_file_or_directory.zip my_resource_file_or_directory/
```

3. Store your resource in a couple of cloud storage services, and get their download URL. It is recommended to store your resource in at least two distinct cloud providers.

4. Hash your resource by using SHA256 from Python hashlib, as follows:

```python
import hashlib

def produce_hash(model_uri: str) -> str:
    read_block_size_in_bytes = 64 * 1024 * 1024  # Read in blocks of 64MiB; any amount will work.
    hasher = hashlib.sha256()
    
    with open(model_uri, "rb") as f_in:
        for data_chunk in iter(lambda: f_in.read(read_block_size_in_bytes), b""):
            hasher.update(data_chunk)
    
    return hasher.hexdigest()

my_resource_sha256 = produce_hash("path/to/my_resource.zip")
print(my_resource_sha256)
```

5. Register your resource in a `JSON` file within the [trusted_urls directory](./buscador/trusted_urls/), providing the resource task, resource name, file extension (`.zip` or `.tar` for compressed resources), SHA256, and the direct download URLs as depicted in the exemple below (use [buscador/trusted_urls/models.json](./buscador/trusted_urls/models.json) as an exemple). You can either create a new `JSON` file or register your resource in an existing file, as long as you keep your resource semantically coherent with the configuration filename. Also note that Ulysses Fetcher will try to download resources by following the provided order in `urls`. Hence, later URLs are fallback addresses in case something went wrong with every previous URL.

```json
{
  "task_name": {
    "resource_name": {
      "sha256": "<my_resource_sha256>",
      "file_extension": ".zip",
      "urls": [
        "https://url_1",
        "https://url_2",
        "..."
      ]
    }
  }
}
```

6. Create a Pull Request with your changes, providing all information about your resource. Your contribution will be reviewed and, if appropriate to this library, it may get accepted.

---

## License
[MIT.](./LICENSE)
