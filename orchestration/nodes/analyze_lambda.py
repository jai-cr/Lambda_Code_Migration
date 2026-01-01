# orchestration/nodes/analyze_lambda.py
from llm.client import call_llm
from prompts.loader import load_prompt
from orchestration.state import MigrationState
import json

PROMPT1 = load_prompt(
    category="analysis",
    name="classify_lambda"
)

PROMPT2 = load_prompt(
    category="analysis",
    name="extract_entrypoints"
)

PROMPT3 = load_prompt(
    category="analysis",
    name="identify_aws_services"
)

def analyze_lambda(state: MigrationState) -> MigrationState:

    handler_file = state["handler_files"]  # e.g. OrderHandler.java
    handler_code = state["java_files"]

#    supporting_code = "\n\n".join(
#        code for name, code in state["java_files"].items()
#        if name != handler_file
#    )

    response_text = call_llm(
        system_prompt="You are a senior Java AWS Lambda expert.",
        user_prompt=PROMPT1.format(
            handler_code=handler_code,
            #supporting_code=supporting_code,
            dependencies=state["dependencies"]
        ),
        response_format="json"
    )

    with open("migration_results.txt", "a") as f:
        print("First response", file =f)
        print(response_text, file=f)
    response = json.loads(response_text)
    state["lambda_type"] = response["lambda_type"]

    response_text = call_llm(
        system_prompt="You are a senior Java AWS Lambda expert.",
        user_prompt=PROMPT2.format(
            handler_code=handler_code,
            dependencies=state["dependencies"]
        ),
        response_format="json"
    )
    with open("migration_results.txt", "a") as f:
        print("Second response", file =f)
        print(response_text, file=f)
    response = json.loads(response_text)
    state["spring_entrypoints"] = response["entrypoints"]

    response_text = call_llm(
        system_prompt="You are a senior Java AWS Lambda expert.",
        user_prompt=PROMPT3.format(
            handler_code=handler_code,
            dependencies=state["dependencies"]
        ),
        response_format="json"
    )
    with open("migration_results.txt", "a") as f:
        print("Third response", file =f)
        print(response_text, file=f)
    response = json.loads(response_text)
    state["aws_services"] = response["aws_services"]

    return state
