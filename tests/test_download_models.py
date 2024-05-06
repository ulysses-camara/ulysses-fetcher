"""Check if resources can be downloaded corrctly."""
import os
import shutil
import glob
import time

import pytest

import buscador


def test_trusted_urls_integrity():
    """Check if all resource URLs and SHA256 hashes are unique."""
    all_hashes = set()
    all_urls = set()

    for _, task_resources in buscador.DEFAULT_URIS.items():
        for _, task_metadata in task_resources.items():
            cur_sha256 = task_metadata["sha256"]
            cur_urls = task_metadata["urls"]

            assert cur_sha256 not in all_hashes
            all_hashes.add(cur_sha256)

            for url in cur_urls:
                assert url not in all_urls
                all_urls.add(url)


@pytest.mark.parametrize(
    "resource_name,task_name",
    [
        ("bill_summary_to_topics", "sentence_model_evaluation"),
        ("code_estatutes_cf88", "sentence_model_evaluation"),
        ("factnews_news_bias", "sentence_model_evaluation"),
        ("factnews_news_factuality", "sentence_model_evaluation"),
        ("fakebr_size_normalized", "sentence_model_evaluation"),
        ("faqs", "sentence_model_evaluation"),
        ("hatebr_offensive_lang", "sentence_model_evaluation"),
        ("masked_law_name_in_news", "sentence_model_evaluation"),
        ("masked_law_name_in_summaries", "sentence_model_evaluation"),
        ("oab_first_part", "sentence_model_evaluation"),
        ("oab_second_part", "sentence_model_evaluation"),
        ("offcombr2", "sentence_model_evaluation"),
        ("stj_summary", "sentence_model_evaluation"),
        ("sts_state_news", "sentence_model_evaluation"),
        ("summary_vs_bill", "sentence_model_evaluation"),
        ("tampered_leg", "sentence_model_evaluation"),
        ("trf_examinations", "sentence_model_evaluation"),
        ("ulysses_sd", "sentence_model_evaluation"),

        ("4_layer_6000_vocab_size_bert_v3", "legal_text_segmentation"),
        ("2_layer_6000_vocab_size_bert_v3", "legal_text_segmentation"),
        ("256_hidden_dim_6000_vocab_size_1_layer_lstm_v3", "legal_text_segmentation"),
        ("6000_subword_tokenizer", "legal_text_segmentation"),

        ("ulysses_LaBSE_30000", "sentence_similarity"),
        ("sbert_1mil_anama", "sentence_similarity"),
        ("sbert_650k_nheeng", "sentence_similarity"),
        ("sbert_map2doc_v1", "sentence_similarity"),
        ("legal_sroberta_v0", "sentence_similarity"),
        ("legal_sroberta_v1", "sentence_similarity"),

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
        ("dataset_sp_court_cases_bigram_shift_v1", "probing_task"),
        ("dataset_sp_court_cases_coordination_inversion_v1", "probing_task"),
        ("dataset_sp_court_cases_obj_number_v1", "probing_task"),
        ("dataset_sp_court_cases_odd_man_out_v1", "probing_task"),
        ("dataset_sp_court_cases_past_present_v1", "probing_task"),
        ("dataset_sp_court_cases_sentence_length_v1", "probing_task"),
        ("dataset_sp_court_cases_subj_number_v1", "probing_task"),
        ("dataset_sp_court_cases_top_constituents_v1", "probing_task"),
        ("dataset_sp_court_cases_tree_depth_v1", "probing_task"),
        ("dataset_sp_court_cases_word_content_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_bigram_shift_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_coordination_inversion_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_obj_number_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_odd_man_out_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_past_present_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_sentence_length_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_subj_number_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_top_constituents_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_tree_depth_v1", "probing_task"),
        ("dataset_political_speeches_ptbr_word_content_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_bigram_shift_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_coordination_inversion_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_obj_number_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_odd_man_out_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_past_present_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_sentence_length_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_subj_number_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_top_constituents_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_tree_depth_v1", "probing_task"),
        ("dataset_leg_pop_comments_ptbr_word_content_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_bigram_shift_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_coordination_inversion_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_obj_number_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_odd_man_out_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_past_present_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_sentence_length_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_subj_number_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_top_constituents_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_tree_depth_v1", "probing_task"),
        ("dataset_leg_docs_ptbr_word_content_v1", "probing_task"),
        ("political_brsd_v0", "stance_detection"),
    ],
)
def test_download_resources(resource_name: str, task_name: str):
    output_dir = os.path.join(os.path.dirname(__file__), "downloaded_resources_from_tests")

    has_succeed = buscador.download_resource(
        task_name=task_name,
        resource_name=resource_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=False,
        clean_compressed_files=True,
        check_resource_hash=True,
        timeout_limit_seconds=60,
    )

    output_uri = os.path.join(output_dir, resource_name)

    def check_file_exists(path: str) -> bool:
        for ext in ("", ".pt", ".csv"):
            if os.path.exists(f"{path}{ext}"):
                return True
        return False

    assert has_succeed
    assert check_file_exists(output_uri), output_uri

    t_start = time.perf_counter()

    has_succeed = buscador.download_resource(
        task_name=task_name,
        resource_name=resource_name,
        output_dir=output_dir,
        show_progress_bar=False,
        check_cached=True,
        clean_compressed_files=True,
        check_resource_hash=True,
        timeout_limit_seconds=60,
    )

    t_delta = time.perf_counter() - t_start

    assert t_delta <= 1.0, t_delta
    assert has_succeed
    assert check_file_exists(output_uri), output_uri

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
        timeout_limit_seconds=60,
    )

    t_delta = time.perf_counter() - t_start

    assert t_delta <= 1.0, t_delta
    assert has_succeed
    assert os.path.exists(output_uri), output_uri

    shutil.rmtree(output_dir)


def test_get_available_tasks():
    assert buscador.get_available_tasks()


@pytest.mark.parametrize(
    "task_name",
    [
        "legal_text_segmentation",
        "sentence_similarity",
        "probing_task",
        "sentence_model_evaluation",
    ],
)
def test_get_available_resources_for_segmentation_task(task_name: str):
    assert buscador.get_task_available_resources(task_name=task_name)
