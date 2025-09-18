"""Prompt utilities for loading and con    # Read and return the content
try:
    with open(prompt_file, encoding='utf-8') as file:
        content = file.read().strip()
        return content
except Exception as e:
    raise RuntimeError(
        f"Error reading prompt file {prompt_file}: {e}"
    ) from e markdown prompts"""

from pathlib import Path
from typing import Optional


def load_prompt_from_markdown(
    prompt_name: str, prompts_dir: Optional[str] = None
) -> str:
    """
    Load a prompt from a markdown file and convert it to a string.

    Args:
        prompt_name: Name of the prompt file (without .md extension)
        prompts_dir: Optional custom prompts directory path

    Returns:
        str: The prompt content as a string

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        ValueError: If prompt_name is empty
    """
    if not prompt_name:
        raise ValueError("Prompt name cannot be empty")

    # Default to src/prompts directory
    if prompts_dir is None:
        current_dir = Path(__file__).parent
        prompts_dir = current_dir.parent / "prompts"
    else:
        prompts_dir = Path(prompts_dir)

    # Construct the full path to the markdown file
    prompt_file = prompts_dir / f"{prompt_name}.md"

    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    # Read and return the content
    try:
        with open(prompt_file, encoding="utf-8") as file:
            content = file.read().strip()
            return content
    except Exception as e:
        raise RuntimeError(f"Error reading prompt file {prompt_file}: {e}")


def list_available_prompts(prompts_dir: Optional[str] = None) -> list[str]:
    """
    List all available prompt files in the prompts directory.

    Args:
        prompts_dir: Optional custom prompts directory path

    Returns:
        list[str]: List of prompt names (without .md extension)
    """
    # Default to src/prompts directory
    if prompts_dir is None:
        current_dir = Path(__file__).parent
        prompts_dir = current_dir.parent / "prompts"
    else:
        prompts_dir = Path(prompts_dir)

    if not prompts_dir.exists():
        return []

    # Find all .md files and return their names without extension
    prompt_files = []
    for file in prompts_dir.glob("*.md"):
        prompt_files.append(file.stem)

    return sorted(prompt_files)


def validate_prompt_content(content: str) -> bool:
    """
    Validate that prompt content is not empty and contains meaningful text.

    Args:
        content: The prompt content to validate

    Returns:
        bool: True if content is valid, False otherwise
    """
    if not content or not content.strip():
        return False

    # Check if content has more than just whitespace and basic markdown
    cleaned_content = content.strip()
    if len(cleaned_content) < 10:  # Minimum meaningful content length
        return False

    return True


# Convenience function for common use case
def get_prompt(prompt_name: str) -> str:
    """
    Convenience function to get a prompt with validation.

    Args:
        prompt_name: Name of the prompt file

    Returns:
        str: The validated prompt content

    Raises:
        ValueError: If prompt content is invalid
    """
    content = load_prompt_from_markdown(prompt_name)

    if not validate_prompt_content(content):
        raise ValueError(f"Invalid or empty prompt content in {prompt_name}.md")

    return content
