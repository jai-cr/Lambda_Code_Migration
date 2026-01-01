# orchestration/nodes/reconcile_files.py
from llm.client import call_llm
from prompts.migration.reconcile_files import PROMPT

def reconcile_files(state: MigrationState) -> MigrationState:
    response = call_llm(
        prompt=PROMPT,
        variables={
            "files": state["migrated_files"],
            "blueprint": state["spring_blueprint"]
        }
    )

    state["migrated_files"] = response["files"]
    return state
