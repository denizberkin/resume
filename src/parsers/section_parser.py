import re
from pathlib import Path
from typing import Dict, List, Tuple

from .latex_cleaner import LaTeXCleaner


class SectionParser:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.sections_dir = base_dir / "sections"
        self.cleaner = LaTeXCleaner()

    def parse_file(self, filename: str) -> Dict:
        filepath = self.sections_dir / filename

        if not filepath.exists():
            return {"subsections": []}

        content = filepath.read_text(encoding="utf-8")
        content = self.cleaner.remove_document_wrapper(content)

        if "\\subsection" in content:
            return self._parse_subsections(content)
        else:
            return self._parse_direct_content(content)

    def _parse_subsections(self, content: str) -> Dict:
        section_data = {"subsections": []}

        subsection_pattern = r"\\subsection\{(.*?)\}(.*?)(?=\\subsection|\Z)"
        subsections = re.findall(subsection_pattern, content, re.DOTALL)

        for title_raw, body in subsections:
            title, date = self._parse_subsection_header(title_raw)

            subsection = {
                "title": title,
                "date": date,
                "subtext": self._extract_subtext(body),
                "items": self._extract_items(body),
            }

            section_data["subsections"].append(subsection)

        return section_data

    def _parse_direct_content(self, content: str) -> Dict:
        lines = []

        for line in content.split("\n"):
            line = line.strip()

            # Skip empty lines and pure LaTeX commands
            if not line or line.startswith("%"):
                continue

            # Include lines with content or formatting
            if not line.startswith("\\") or any(cmd in line for cmd in ["\\textit", "\\hfill", "\\scriptsize"]):
                cleaned = self.cleaner.clean(line)
                if cleaned:
                    lines.append(cleaned)

        return {"direct_content": " ".join(lines)} if lines else {}

    def _parse_subsection_header(self, title: str) -> Tuple[str, str]:
        parts = re.split(r"\\hfill", title)

        job_title = parts[0].strip()
        date = ""

        if len(parts) > 1:
            date_part = parts[1].strip()

            # Try multiple date patterns
            date_patterns = [
                r"\\textit\{\\textmd\{([^}]+)\}\}",  # Standard format
                r"\\textit\{([^}]+)\}",  # Without \textmd
                r"\\textmd\{([^}]+)\}",  # Without \textit
            ]

            for pattern in date_patterns:
                date_match = re.search(pattern, date_part)
                if date_match:
                    date = date_match.group(1).strip()
                    break

            # Fallback to cleaned text
            if not date:
                date = self.cleaner.clean(date_part)

        return self.cleaner.clean(job_title), date

    def _extract_subtext(self, body: str) -> str:
        subtext_match = re.search(r"\\subtext\{([^}]*)\}", body)
        if subtext_match:
            return self.cleaner.clean(subtext_match.group(1))
        return ""

    def _extract_items(self, body: str) -> List[str]:
        items_match = re.search(r"\\begin\{zitemize\}(.*?)\\end\{zitemize\}", body, re.DOTALL)

        if not items_match:
            return []

        items_text = items_match.group(1)
        items = re.findall(r"\\item\s+(.+?)(?=\\item|\Z)", items_text, re.DOTALL)

        return [self.cleaner.clean(item.strip()) for item in items if item.strip()]
