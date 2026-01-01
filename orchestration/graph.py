# orchestration/graph.py
from langgraph.graph import StateGraph, END
from orchestration.state import MigrationState
from orchestration.nodes.analyze_lambda import analyze_lambda
#from orchestration.nodes.compile_and_test import compile_and_test
from orchestration.nodes.generate_blueprint import generate_blueprint
from orchestration.nodes.migrate_class import migrate_class
#from orchestration.nodes.reconcile_files import reconcile_files
#from orchestration.nodes.fix_errors import fix_errors
from analysis.java_parser import extract_chunks_for_lambda
from analysis.pom_parser import parse_pom_dependencies
from pathlib import Path
from execution.diff_writer import write_migrated_files
from IPython.display import Image, display

def has_more_files(state: MigrationState):
    return (
        "migrate"
        if state.current_index + 1 < len(state.handler_files)
        else END
    )

def increment_index(state: MigrationState):
    state.current_index += 1
    return state

graph = StateGraph(MigrationState)

graph.add_node("analyze", analyze_lambda)
graph.add_node("blueprint", generate_blueprint)
graph.add_node("increment", increment_index)

graph.add_node("migrate", migrate_class)
#graph.add_node("reconcile", reconcile_files)
#graph.add_node("compile", compile_and_test)
#graph.add_node("fix", fix_errors)

graph.set_entry_point("analyze")

graph.add_edge("analyze", "blueprint")
graph.add_edge("blueprint", "migrate")
graph.add_edge("migrate", END)
"""
graph.add_conditional_edges(
    "increment",
    has_more_files,
    {
        "migrate": "migrate",
        END: END
    }
)
"""

#graph.add_edge("migrate", "reconcile")
#graph.add_edge("migrate", END)
#graph.add_edge("reconcile", "compile")

#graph.add_conditional_edges(
#    "compile",
#    lambda s: "fix" if s["compile_errors"] and s["iteration"] < 3 else END,
#    {
#        "fix": "fix"
#    }
#)

#graph.add_edge("fix", "compile")

migration_app = graph.compile()
# Generate the PNG data
png_data = migration_app.get_graph().draw_mermaid_png()

# Save it to a file
with open("graph_visualization.png", "wb") as f:
    f.write(png_data)
print("Hello from migration!")
lambda_root = "input/api-login-lambda"
chunks = extract_chunks_for_lambda(Path(lambda_root))
pom_path = lambda_root + "/pom.xml"
pom_metadata = parse_pom_dependencies(pom_path)


result = migration_app.invoke({
    "lambda_name": lambda_root[6:],
    "handler_files": list(chunks),
    "java_files": chunks,
    "dependencies": pom_metadata,
    "current_index": 1,
    "iteration": 1
})


write_migrated_files(
    output_root=Path("output") / result["lambda_name"],
    base_package=result["spring_package"],
    migrated_files=result["migrated_files"]
)
"""
write_migrated_files(
    output_root=Path("output") / lambda_root[6:],
    base_package="com.example.app",
    migrated_files=chunks
)
"""
