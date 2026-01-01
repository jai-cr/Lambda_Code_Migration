import subprocess
from pathlib import Path
from typing import List

class MavenExecutor:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def clean_package(self) -> dict:
        cmd = ["mvn", "clean", "package", "-DskipTests"]

        process = subprocess.Popen(
            cmd,
            cwd=self.project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        errors = self._extract_compile_errors(stdout + stderr)

        return {
            "success": process.returncode == 0,
            "errors": errors,
            "raw_output": stdout + stderr
        }

    def _extract_compile_errors(self, output: str) -> List[str]:
        """
        Extracts javac errors only (filters noise).
        """
        errors = []
        capture = False

        for line in output.splitlines():
            if "[ERROR]" in line:
                capture = True
                errors.append(line)
            elif capture and line.strip().startswith("^"):
                errors.append(line)

        return errors
