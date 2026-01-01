# orchestration/state.py
from typing import TypedDict, Dict, List

class MigrationState(TypedDict):
    lambda_name: str
    handler_files: List[str]
    java_files: Dict[str, str]          # filename -> source
    dependencies: List[str]
    aws_services: List[str]
    lambda_type: str                    # api / event / batch
    spring_blueprint: Dict
    migrated_files: Dict[str, str]
    compile_errors: List[str]
    iteration: int
    current_index: int = 0
    current_file: str | None = None
    spring_package: str | None = None
    spring_role: str | None = None
    spring_entrypoints: List[str]
