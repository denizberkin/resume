import re
from pathlib import Path
from typing import Dict


class HTMLUpdater:
    def __init__(self, html_path: Path):
        self.html_path = html_path
        self.content = ""

        if html_path.exists():
            self.content = html_path.read_text(encoding="utf-8")

    def update_section(self, section_id: str, new_content: str) -> bool:
        patterns = {
            "work": r'(<section id="work".*?<h2.*?>.*?</h2>\s*)(.*?)(\s*</section>)',
            "education": r'(<section id="education".*?<h2.*?>.*?</h2>\s*)(.*?)(\s*</section>)',
            "projects": r'(<section id="projects".*?<h2.*?>.*?</h2>\s*)(.*?)(\s*</section>)',
            "skills": r'(<section id="skills".*?<div class="skills-grid">\s*)(.*?)(\s*</div>\s*</section>)',
        }

        if section_id not in patterns:
            return False

        pattern = patterns[section_id]

        # different replacement formats for different sections
        if section_id == "skills":
            replacement = r"\g<1>\n" + new_content + r"\n                \g<3>"
        elif section_id == "education":
            replacement = r"\g<1>" + new_content + r"\g<3>"
        else:
            replacement = r"\g<1>\n                " + new_content + r"\n            \g<3>"

        new_content_str = re.sub(pattern, replacement, self.content, flags=re.DOTALL)

        # check if anything was actually replaced
        if new_content_str == self.content:
            return False

        self.content = new_content_str
        return True

    def update_contact_info(self, contact: Dict[str, str]) -> bool:
        success = True

        # update name
        if "name" in contact:
            self.content = self.content.replace("<div>Berkin Deniz Kahya</div>", f"<div>{contact['name']}</div>")

        # update email
        if "email" in contact:
            self.content = re.sub(
                r'<div><a href="mailto:[^"]*"[^>]*>[^<]*</a></div>',
                f'<div><a href="mailto:{contact["email"]}" style="color: white;">{contact["email"]}</a></div>',
                self.content,
            )

        # update location
        if "city" in contact:
            self.content = re.sub(r"<div>İstanbul, Turkey</div>", f"<div>{contact['city']}</div>", self.content)

        return success

    def save(self) -> bool:
        try:
            self.html_path.write_text(self.content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"Error saving HTML file: {e}")
            return False

    def backup(self, backup_path: Path = None) -> bool:
        if backup_path is None:
            backup_path = self.html_path.with_suffix(".html.bak")

        try:
            if self.html_path.exists():
                original_content = self.html_path.read_text(encoding="utf-8")
                backup_path.write_text(original_content, encoding="utf-8")
                return True
        except Exception as e:
            print(f"Error creating backup: {e}")

        return False

    def validate_structure(self) -> bool:
        required_sections = ["work", "education", "projects", "skills"]

        for section_id in required_sections:
            pattern = f'<section id="{section_id}"'
            if pattern not in self.content:
                print(f"Warning: Section '{section_id}' not found in HTML")
                return False

        return True
