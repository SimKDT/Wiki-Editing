import re
from pathlib import Path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Edit for delete script")
    parser.add_argument("directory", type=Path, help="Directory to edit for delete")
    args = parser.parse_args()

    base_delete_template = r"{{Delete|This parameter's wiki documentation may be outdated and has been moved to the [[PZ API Documentation]] and this page will be deleted in the future.}}"

    directory: Path = args.directory

    if not directory.exists() or not directory.is_dir():
        parser.error(f"Directory not found: {directory}")

    for file in directory.iterdir():
        if not file.is_file():
            continue

        print(f"Editing file for delete: {file}")
        with open(file, "r") as f:
            content = f.read()

        # add a delete template after "{{Page version|...}}"
        content = re.sub(r"(\{\{Page version\|.*?\}\})", r"\1\n" + base_delete_template, content)

        with open(file, "w") as f:
            f.write(content)

if __name__ == "__main__":
    main()