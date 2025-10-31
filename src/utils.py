def append_indentation(text: str, spaces: str) -> str:
    """append indentation to each line of the input to simulate indentation"""
    indented_lines = [
        spaces + line if line.strip() != "" and i != 0 else line for i, line in enumerate(text.splitlines())
    ]  # skip indenting the first line
    return "\n".join(indented_lines)
