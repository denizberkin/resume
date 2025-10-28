import re


class LaTeXCleaner:
    """Clean LaTeX syntax"""

    def __init__(self):
        """Initialize the cleaner with conversion rules"""
        self.conversion_rules = self._build_conversion_rules()

    def _build_conversion_rules(self) -> list:
        """Build list of (pattern, replacement) tuples for conversion"""
        return [
            # Remove comments
            (r"%.*$", "", re.MULTILINE),
            # Special characters
            (r"\\&", "&amp;", 0),
            (r"\\%", "%", 0),
            (r"\$\\sim\$", "~", 0),
            # Formatting commands
            (r"\\textit\{([^}]+)\}", r"<em>\1</em>", 0),
            (r"\\textbf\{([^}]+)\}", r"<strong>\1</strong>", 0),
            (r"\\textmd\{([^}]+)\}", r"\1", 0),
            # Size commands (remove)
            (r"\\(scriptsize|tiny|small|large|Large|LARGE|huge|Huge)\s*\{?\}?", "", 0),
            # Layout commands
            (r"\\hfill", "", 0),
        ]

    def clean(self, text: str) -> str:
        # Apply basic conversion rules
        for pattern, replacement, flags in self.conversion_rules:
            text = re.sub(pattern, replacement, text, flags=flags)

        # Handle hyperlinks with custom function
        text = self._convert_hyperlinks(text)

        # Handle external link icon
        text = re.sub(r"\\externallink", '<i class="fas fa-external-link-alt"></i>', text)

        return text.strip()

    def _convert_hyperlinks(self, text: str) -> str:
        def replace_href(match: re.Match) -> str:
            url = match.group(1)
            link_text = match.group(2)
            # Remove nested color commands
            link_text = re.sub(r"\\color\{[^}]+\}\{?([^}]+)\}?", r"\1", link_text)
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{link_text}</a>'

        return re.sub(r"\\href\{([^}]+)\}\{([^}]+)\}", replace_href, text)

    def extract_from_command(self, text: str, command: str) -> str:
        pattern = rf"\\{command}\{{([^}}]+)\}}"
        match = re.search(pattern, text)
        return match.group(1) if match else ""

    def remove_document_wrapper(self, text: str) -> str:
        text = re.sub(r"\\documentclass.*?\\begin\{document\}", "", text, flags=re.DOTALL)
        text = re.sub(r"\\end\{document\}", "", text)
        return text
