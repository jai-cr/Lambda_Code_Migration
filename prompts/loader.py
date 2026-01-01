from pathlib import Path

PROMPT_ROOT = Path(__file__).parent

def load_prompt(category: str, name: str) -> str:
    """
    Example:
      load_prompt("spring", "generate_project_structure")
    """
    prompt_path = PROMPT_ROOT / category / f"{name}.txt"

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")
