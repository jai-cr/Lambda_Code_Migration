# orchestration/nodes/compile_and_test.py
from orchestration.state import MigrationState
from execution.maven_executor import compile_project

def compile_and_test(state: MigrationState) -> MigrationState:
    errors = compile_project(
        files=state["migrated_files"],
        project_name=state["lambda_name"]
    )

    state["compile_errors"] = errors
    return state
