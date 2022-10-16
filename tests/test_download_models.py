"""Check if resources can be downloaded corrctly."""
import os
import shutil
import glob
import time

import pytest

import buscador


@pytest.mark.parametrize(
    "resource_name,task_name",
    [
        ("2_layer_6000_vocab_size_bert", "legal_text_segmentation"),
        ("512_hidden_dim_6000_vocab_size_1_layer_lstm", "legal_text_segmentation"),
        ("6000_subword_tokenizer", "legal_text_segmentation"),
        ("distil_sbert_br_ctimproved_12_epochs_v1", "sentence_similarity"),
        ("dataset_wikipedia_ptbr_bigram_shift_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_coordination_inversion_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_obj_number_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_odd_man_out_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_past_present_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_sentence_length_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_subj_number_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_top_constituents_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_tree_depth_v1", "probing_task"),
        ("dataset_wikipedia_ptbr_word_content_v1", "probing_task"),
    ],
)
def test_download_segmenter_resources(resource_name: str, task_name: str):
    output_dir = os.path.join(os.path.dirname(__file__), "downloaded_resources_from_tests")

    has_succeed = buscador.download_resource(
        task_name=task_name,
        resource_name=resource_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=False,
        clean_compressed_files=True,
        check_resource_hash=True,
    )

    output_uri = os.path.join(output_dir, resource_name)

    assert has_succeed
    assert os.path.exists(output_uri) or os.path.exists(f"{output_uri}.pt")

    t_start = time.perf_counter()

    has_succeed = buscador.download_resource(
        task_name=task_name,
        resource_name=resource_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=True,
        clean_compressed_files=True,
        check_resource_hash=True,
    )

    t_delta = time.perf_counter() - t_start

    assert t_delta <= 1.0, t_delta
    assert has_succeed
    assert os.path.exists(output_uri) or os.path.exists(f"{output_uri}.pt"), output_uri

    if os.path.isdir(output_uri):
        shutil.rmtree(output_dir)

    else:
        for uri in glob.glob(f"{output_uri}*"):
            os.remove(uri)

        os.rmdir(output_dir)


def test_keep_compressed_file():
    resource_name = "6000_subword_tokenizer"
    output_dir = os.path.join(os.path.dirname(__file__), "downloaded_resources_from_tests")

    has_succeed = buscador.download_resource(
        task_name="legal_text_segmentation",
        resource_name=resource_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=False,
        clean_compressed_files=False,
        check_resource_hash=True,
    )

    output_uri = os.path.join(output_dir, resource_name)

    assert has_succeed
    assert os.path.exists(output_uri), output_uri
    assert os.path.isfile(os.path.join(output_dir, f"{resource_name}.zip"))

    t_start = time.perf_counter()

    has_succeed = buscador.download_resource(
        task_name="legal_text_segmentation",
        resource_name=resource_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=True,
        clean_compressed_files=False,
        check_resource_hash=True,
    )

    t_delta = time.perf_counter() - t_start

    assert t_delta <= 1.0, t_delta
    assert has_succeed
    assert os.path.exists(output_uri), output_uri

    shutil.rmtree(output_dir)


def test_get_available_tasks():
    assert buscador.get_available_tasks()


@pytest.mark.parametrize(
    "task_name", ["legal_text_segmentation", "sentence_similarity", "probing_task"]
)
def test_get_available_resources_for_segmentation_task(task_name: str):
    assert buscador.get_task_available_resources(task_name=task_name)
