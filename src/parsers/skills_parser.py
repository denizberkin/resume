import re
from pathlib import Path
from typing import Dict, List

from .latex_cleaner import LaTeXCleaner


class SkillsParser:
    """Parse skills section with tabular format"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.skills_path = base_dir / "sections" / "skills.tex"
        self.cleaner = LaTeXCleaner()

    def parse(self) -> Dict[str, List[str]]:
        if not self.skills_path.exists():
            return {}

        content = self.skills_path.read_text(encoding="utf-8")

        tabular_match = re.search(r"\\begin\{tabular\}.*?\\end\{tabular\}", content, re.DOTALL)

        if not tabular_match:
            return {}

        return self._parse_tabular(tabular_match.group(0))

    def _parse_tabular(self, tabular_content: str) -> Dict[str, List[str]]:
        skills_data = {}

        # parse rows: \skills{Category} & & items \\
        rows = re.findall(r"\\skills\{([^}]+)\}\s*&\s*&\s*(.+?)(?:\\\\|\Z)", tabular_content, re.DOTALL)

        for category_raw, items_text_raw in rows:
            category = self.cleaner.clean(category_raw)
            items_text = self.cleaner.clean(items_text_raw)

            # remove trailing size commands
            items_text = re.sub(r"\\(scriptsize|tiny).*$", "", items_text, flags=re.MULTILINE | re.DOTALL)
            items_text = items_text.strip()

            # split by comma and clean
            items = [item.strip() for item in items_text.split(",") if item.strip()]

            if items:
                skills_data[category] = items

        return skills_data

    def get_categories(self, skills_data: Dict[str, List[str]]) -> List[str]:
        """Get list of skill categories"""
        return list(skills_data.keys())

    def get_skills_count(self, skills_data: Dict[str, List[str]]) -> int:
        """Get total number of skills across all categories"""
        return sum(len(skills) for skills in skills_data.values())
