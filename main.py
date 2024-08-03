import argparse
import fnmatch
import hashlib
import os
import sys
from typing import Literal, get_args

Comparison = Literal["content", "name", "size"]
DEFAULT_COMPARISON: tuple[Comparison, ...] = ("name", "size")


def filter_file_by_pattern(
    file: str,
    file_patterns: list[str] | None = None,
    exclude_file_patterns: list[str] | None = None,
) -> bool:
    for pattern in file_patterns or []:
        if not fnmatch.fnmatch(file, pattern):
            return False
    for pattern in exclude_file_patterns or []:
        if fnmatch.fnmatch(file, pattern):
            return False
    return True


def find_dups(
    folders: list[str],
    comparison_type: tuple[Comparison, ...] = DEFAULT_COMPARISON,
    file_patterns: list[str] | None = None,
    exclude_file_patterns: list[str] | None = None,
) -> None:
    for folder in folders:
        if not os.path.isdir(folder):
            raise ValueError(f"folder {folder} does not exists")

    files_map: dict[int, list[str]] = {}
    for folder in folders:
        for root, _, files in os.walk(folder):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_path_abs = os.path.abspath(file_path)
                if not filter_file_by_pattern(
                    file_path_abs, file_patterns, exclude_file_patterns
                ):
                    continue

                hash_ = 0
                if "content" in comparison_type:
                    with open(file_path_abs, "rb") as fh:
                        hash_ += int(hashlib.sha256(fh.read()).hexdigest(), 16)
                if "name" in comparison_type:
                    hash_ += int(hashlib.sha256(filename.encode()).hexdigest(), 16)
                if "size" in comparison_type:
                    hash_ += os.stat(file_path_abs).st_size

                try:
                    files_map[hash_].append(file_path_abs)
                except KeyError:
                    files_map[hash_] = [file_path_abs]
    dup_cnt = 0
    for files in files_map.values():
        if len(files) > 1:
            dup_cnt += 1
            print(f"duplicate {dup_cnt}:")
            for file in files:
                print("    ", file, sep="")
    print(f"found {dup_cnt} duplicates")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "dup_finder",
        description="program to find and remove file duplicates in a directory",
        epilog="usage example: python3 dup_finder -c content -p '*.csv' '*.json' -i -- folder1 folder2",
    )
    parser.add_argument(
        "folders",
        nargs="+",
        action="extend",
        help="folder used to search",
    )
    parser.add_argument(
        "-c",
        "--comparison-type",
        dest="comparison",
        choices=get_args(Comparison),
        default=list(DEFAULT_COMPARISON),
        nargs="*",
        help="comparison used to target duplicates. Defaults to name and size",
    )

    parser.add_argument(
        "-p",
        "--file-pattern",
        dest="patterns",
        nargs="*",
        action="extend",
        help="file pattern used to restrict search",
    )
    parser.add_argument(
        "-x",
        "--exclude-file-pattern",
        dest="exclude",
        nargs="*",
        action="extend",
        help="file pattern used to exclude from search",
    )
    args = parser.parse_args()
    try:
        find_dups(
            folders=args.folders,
            comparison_type=tuple(args.comparison),
            file_patterns=args.patterns,
            exclude_file_patterns=args.exclude,
        )
    except Exception as exp:
        print("program encountered an error:", exp, file=sys.stderr)
        raise SystemExit(1)
