import re
import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

load_dotenv()


class ContactParser:
    PATTERNS = {
        "name": r"\\def\\name\{([^}]+)\}",
        "phone": r"\\def\\phone\{([^}]+)\}",
        "city": r"\\def\\city\{([^}]+)\}",
        "email": r"\\def\\email\{([^}]+)\}",
        "linkedin": r"\\def\\LinkedIn\{([^}]+)\}",
        "github": r"\\def\\github\{([^}]+)\}",
        "kaggle": r"\\def\\kaggle\{([^}]+)\}",
        "role": r"\\def\\role\{([^}]*)\}",
    }

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

        # Try to find the main resume file (resume.tex or main.tex or similar)
        possible_names = ["resume.tex", "main.tex", "cv.tex"]
        self.resume_path = None

        for name in possible_names:
            path = base_dir / name
            if path.exists():
                self.resume_path = path
                break

        # Fallback to resume.tex if nothing found
        if self.resume_path is None:
            self.resume_path = base_dir / "resume.tex"

    def parse(self) -> Dict[str, str]:
        if not self.resume_path.exists():
            return {}

        content = self.resume_path.read_text(encoding="utf-8")
        contact = {}

        for key, pattern in self.PATTERNS.items():
            match = re.search(pattern, content)
            if match:
                value = match.group(1).strip()
                if value:  # Only add non-empty values
                    contact[key] = value

        return contact

    def get_full_name(self, contact: Dict[str, str]) -> str:
        """Get full name or default"""
        return contact.get("name", os.getenv("NAME", "default"))

    def get_email(self, contact: Dict[str, str]) -> str:
        """Get email or default"""
        return contact.get("email", os.getenv("EMAIL", "email@example.com"))

    def get_location(self, contact: Dict[str, str]) -> str:
        """Get location or default"""
        return contact.get("city", os.getenv("CITY", "default city"))

    def get_social_links(self, contact: Dict[str, str]) -> Dict[str, str]:
        social = {}
        github = contact.get("github", os.getenv("GITHUB", "default"))
        linkedin = contact.get("linkedin", os.getenv("LINKEDIN", "default"))
        kaggle = contact.get("kaggle", os.getenv("KAGGLE", "default"))

        social["github"] = f"https://github.com/{github}"
        social["linkedin"] = f"https://www.linkedin.com/in/{linkedin}"
        social["kaggle"] = f"https://www.kaggle.com/{kaggle}"
        return social
