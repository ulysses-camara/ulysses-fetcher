"""Fetch pretrained Ulysses models from command line."""
import argparse

from . import download_models


def parse_args() -> argparse.Namespace:
    """Parse user arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m buscador",
        description=(
            "Download pretrained models for Ulysses project (from Brazil's Chamber of Deputies)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    valid_tasks = download_models.get_available_tasks()

    parser.add_argument(
        "task_name",
        type=str,
        help=(
            "Task name to retrieve a pretrained model from. "
            f"Must be one of the following: {', '.join(valid_tasks)}."
        ),
    )

    parser.add_argument(
        "model_name",
        type=str,
        help="Pretrained model name to retrieve.",
    )

    parser.add_argument(
        "--output-dir",
        "-d",
        default="ulysses_pretrained_models",
        type=str,
        help="Output directory to store downloaded models.",
    )

    parser.add_argument(
        "--timeout-limit",
        "-t",
        default=10,
        type=int,
        help="Timeout limit for stale downloads, in seconds.",
    )

    parser.add_argument(
        "--disable-progress-bar",
        action="store_true",
    )

    parser.add_argument(
        "--ignore-cached-files",
        action="store_true",
    )

    parser.add_argument(
        "--keep-zip-files",
        action="store_true",
    )

    parser.add_argument(
        "--ignore-model-hash",
        action="store_true",
    )

    return parser.parse_args()


def main() -> None:
    """Fetch a pretrained model."""
    args = parse_args()

    has_succeed = download_models.download_model(
        task_name=args.task_name,
        model_name=args.model_name,
        output_dir=args.output_dir,
        show_progress_bar=not args.disable_progress_bar,
        check_cached=not args.ignore_cached_files,
        clean_zip_files=not args.keep_zip_files,
        check_model_hash=not args.ignore_model_hash,
        timeout_limit_seconds=args.timeout_limit,
    )

    if has_succeed:
        print(f"Model downloaded sucessfully in '{args.output_dir}'.")

    else:
        print("Could not download file.")


if __name__ == "__main__":
    main()
