# orchestration/nodes/generate_blueprint.py
from llm.client import call_llm
from prompts.loader import load_prompt
from orchestration.state import MigrationState
import json

PROMPT = load_prompt(
    category="spring",
    name="generate_project_structure"
)

def generate_blueprint(state: MigrationState) -> MigrationState:
    response_text = call_llm(
        system_prompt="You are a senior Java AWS Lambda and SpringBoot expert.",
        user_prompt=PROMPT.format(
            lambda_classification= state["lambda_type"],
            dependencies= state["dependencies"],
            entry_points= state["spring_entrypoints"],
            aws_services= state["aws_services"]
        ),
        response_format="json"
    )
    
    with open("migration_results.txt", "a") as f:
        print("Blueprint response", file =f)
        print(response_text, file=f)
    response = json.loads(response_text)
    state["spring_blueprint"] = response
    state["spring_package"] = response["base_package"]
    state["spring_entrypoints"] = response.get("modules", [])
    return state
