# orchestration/nodes/fix_errors.py
from llm.client import call_llm
from prompts.loader import load_prompt
from orchestration.state import MigrationState

PROMPT = load_prompt(
    category="validation",
    name="compile_error_fix"
)

def fix_errors(state: MigrationState) -> MigrationState:
    response = call_llm(
        prompt=PROMPT,
        variables={
            "files": state["migrated_files"],
            "errors": state["compile_errors"]
        }
    )

    state["migrated_files"] = response["files"]
    state["iteration"] += 1
    return state
