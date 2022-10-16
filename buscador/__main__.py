"""Fetch pretrained Ulysses resources from command line."""
import argparse

from . import download_resources


def parse_args() -> argparse.Namespace:
    """Parse user arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m buscador",
        description=("Download resources for Ulysses project (from Brazil's Chamber of Deputies)."),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    valid_tasks = download_resources.get_available_tasks()

    parser.add_argument(
        "task_name",
        type=str,
        help=(
            "Task name to retrieve a resource from. "
            f"Must be one of the following: {', '.join(valid_tasks)}."
        ),
    )

    parser.add_argument(
        "resource_name",
        type=str,
        help="Pretrained resource name to retrieve.",
    )

    parser.add_argument(
        "--output-dir",
        "-d",
        default="ulysses_resources",
        type=str,
        help="Output directory to store downloaded resources.",
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
        help="if enabled, do not show download progress bar.",
    )

    parser.add_argument(
        "--ignore-cached-files",
        action="store_true",
        help="If enabled, download requested file even if it exists locally.",
    )

    parser.add_argument(
        "--keep-compressed-files",
        action="store_true",
        help="If enabled, keep any compressed files even before decompression.",
    )

    parser.add_argument(
        "--ignore-resource-hash",
        action="store_true",
        help="If enabled, do not verify if downloaded file hash matches the expected value.",
    )

    return parser.parse_args()


def main() -> None:
    """Fetch a resource."""
    args = parse_args()

    has_succeed = download_resources.download_resource(
        task_name=args.task_name,
        resource_name=args.resource_name,
        output_dir=args.output_dir,
        show_progress_bar=not args.disable_progress_bar,
        check_cached=not args.ignore_cached_files,
        clean_compressed_files=not args.keep_compressed_files,
        check_resource_hash=not args.ignore_resource_hash,
        timeout_limit_seconds=args.timeout_limit,
    )

    if has_succeed:
        print(f"Resource downloaded sucessfully in '{args.output_dir}'.")

    else:
        print("Could not download file.")


if __name__ == "__main__":
    main()
