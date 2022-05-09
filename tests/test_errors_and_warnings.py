"""Check if invalid arguments raises proper warnings or exceptions."""
import os

import pytest
import pytest_socket

import buscador


def test_unknown_task_name():
    with pytest.raises(ValueError):
        output_dir = "should_not_exists_dir"

        buscador.download_model(
            task_name="unknown_task_name",
            model_name="6000_subword_tokenizer",
            output_dir=output_dir,
            show_progress_bar=False,
        )

    assert not os.path.isdir(output_dir)


def test_unknown_model_name():
    with pytest.raises(ValueError):
        output_dir = "should_not_exists_dir"

        buscador.download_model(
            task_name="legal_text_segmentation",
            model_name="unknown_model_name",
            output_dir=output_dir,
            show_progress_bar=False,
        )

    assert not os.path.isdir(output_dir)


def test_disabled_connection():
    pytest_socket.disable_socket()

    with pytest.warns(RuntimeWarning, match="Could not download pretrained model"):
        output_dir = "should_not_exists"

        buscador.download_model(
            task_name="legal_text_segmentation",
            model_name="6000_subword_tokenizer",
            output_dir=output_dir,
            show_progress_bar=False,
            check_cached=False,
        )

    assert not os.path.isdir(output_dir)
