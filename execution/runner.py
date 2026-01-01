from pathlib import Path
from execution.maven_executor import MavenExecutor
from execution.diff_writer import DiffWriter

class MigrationRunner:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.maven = MavenExecutor(project_dir)
        self.diff_writer = DiffWriter(project_dir)

    def run(self) -> dict:
        """
        Executes Maven build and captures results.
        """
        result = self.maven.clean_package()

        if result["success"]:
            return {
                "status": "SUCCESS",
                "errors": []
            }

        self.diff_writer.write_compile_errors(result["errors"])
        return {
            "status": "FAILED",
            "errors": result["errors"]
        }
