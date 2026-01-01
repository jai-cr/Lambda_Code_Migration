# orchestration/nodes/migrate_class.py
from llm.client import call_llm
from prompts.loader import load_prompt
from orchestration.state import MigrationState

PROMPT = load_prompt(
    category="migration",
    name="migrate_java_class"
)

def migrate_class(state: MigrationState) -> MigrationState:

    file_name = state["handler_files"][state["current_index"]]
    print(f"file_name {file_name}")
    state["current_file"] = file_name
    chunks = state["java_files"][file_name]
    migrated = {}

   # for file_name, source_code in state["java_files"].items():
    response = call_llm(
        system_prompt="You are a senior Java AWS Lambda and SpringBoot expert.",
        user_prompt=PROMPT.format(
            source_chunks= chunks,
            spring_blueprint= state["spring_blueprint"],
            lambda_type= state["lambda_type"]
        )
    )
    migrated[file_name] = response
    print("Migration call complete")
    state["migrated_files"] = migrated
    return state
