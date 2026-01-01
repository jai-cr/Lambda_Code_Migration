from pathlib import Path
from datetime import datetime
from typing import List


def write_compile_errors(self, errors: List[str]):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    error_file = self.diff_dir / f"compile_errors_{timestamp}.txt"

    with error_file.open("w", encoding="utf-8") as f:
        for err in errors:
            f.write(err + "\n")

def write_diff(self, file_path: Path, before: str, after: str):
    diff_file = self.diff_dir / f"{file_path.name}.diff"

    with diff_file.open("w", encoding="utf-8") as f:
        f.write("----- BEFORE -----\n")
        f.write(before)
        f.write("\n\n----- AFTER -----\n")
        f.write(after)

def write_migrated_files(
    output_root: Path,
    base_package: str,
    migrated_files: dict
):
    base_path = output_root / "src/main/java" / base_package.replace(".", "/")
    base_path.mkdir(parents=True, exist_ok=True)

    for file_name, source in migrated_files.items():
        target = base_path / file_name
        target.write_text(source, encoding="utf-8")

