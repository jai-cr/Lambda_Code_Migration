from pathlib import Path
from typing import Dict, List
import subprocess
import json
from analysis.pom_parser import parse_pom_dependencies

def discover_java_files(lambda_root: Path) -> List[Path]:
    """
    Discover all production Java source files in a Lambda project.
    """
    src_root = lambda_root / "src" / "main" / "java"

    if not src_root.exists():
        raise ValueError(f"Expected Java sources at {src_root}")

    java_files = [
        p for p in src_root.rglob("*.java")
        if not is_excluded_path(p)
    ]

    return java_files


def is_excluded_path(path: Path) -> bool:
    excluded_dirs = {
        "target",
        "build",
        ".git",
        "generated",
        "out"
    }
    return any(part in excluded_dirs for part in path.parts)

def extract_chunks_for_lambda(lambda_root: Path) -> Dict[str, List[Dict]]:
    """
    Returns:
      {
        "OrderHandler.java": [chunks...],
        "OrderService.java": [chunks...]
      }
    """
    java_files = discover_java_files(lambda_root)
    all_chunks = {}

    for java_file in java_files:
        chunks = extract_java_chunks(java_file)
        all_chunks[java_file.name] = chunks

    return all_chunks



SCRIPT_DIR = Path(__file__).parent
JAVA_CHUNKER_JAR = SCRIPT_DIR / "java-chunker-1.0.0.jar"

def extract_java_chunks(java_file: Path) -> List[Dict]:
    try:
        result = subprocess.run(
            ["java", "-jar", JAVA_CHUNKER_JAR, str(java_file)],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Java Error Output: {e.stderr}") # This will show the real error
        raise e

def main():
    print("Hello from migration!")
    lambda_root = "input/api-login-lambda"
    chunks = extract_chunks_for_lambda(Path(lambda_root))
    pom_path = lambda_root / "pom.xml"
    pom_metadata = parse_pom_dependencies(pom_path)
    print(chunks)
    print(pom_metadata)

if __name__ == "__main__":
    main()
