"""Check if models can be downloaded corrctly."""
import os
import shutil
import glob
import time

import pytest

import buscador


@pytest.mark.parametrize(
    "model_name",
    [
        "2_layer_6000_vocab_size_bert",
        "512_hidden_dim_6000_vocab_size_1_layer_lstm",
        "6000_subword_tokenizer",
    ],
)
def test_download_segmenter_models(model_name: str):
    output_dir = os.path.join(os.path.dirname(__file__), "downloaded_models_from_tests")

    has_succeed = buscador.download_model(
        task_name="legal_text_segmentation",
        model_name=model_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=False,
        clean_compressed_files=True,
        check_model_hash=True,
    )

    output_uri = os.path.join(output_dir, model_name)

    assert has_succeed and (os.path.exists(output_uri) or os.path.exists(f"{output_uri}.pt"))

    t_start = time.perf_counter()

    has_succeed = buscador.download_model(
        task_name="legal_text_segmentation",
        model_name=model_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=True,
        clean_compressed_files=True,
        check_model_hash=True,
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
    model_name = "6000_subword_tokenizer"
    output_dir = os.path.join(os.path.dirname(__file__), "downloaded_models_from_tests")

    has_succeed = buscador.download_model(
        task_name="legal_text_segmentation",
        model_name=model_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=False,
        clean_compressed_files=False,
        check_model_hash=True,
    )

    output_uri = os.path.join(output_dir, model_name)

    assert has_succeed
    assert os.path.exists(output_uri), output_uri
    assert os.path.isfile(os.path.join(output_dir, f"{model_name}.zip"))

    t_start = time.perf_counter()

    has_succeed = buscador.download_model(
        task_name="legal_text_segmentation",
        model_name=model_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=True,
        clean_compressed_files=False,
        check_model_hash=True,
    )

    t_delta = time.perf_counter() - t_start

    assert t_delta <= 1.0, t_delta
    assert has_succeed
    assert os.path.exists(output_uri), output_uri

    shutil.rmtree(output_dir)


def test_get_available_tasks():
    assert buscador.get_available_tasks()


def test_get_available_models_for_segmentation_task():
    assert buscador.get_task_available_models(task_name="legal_text_segmentation")
