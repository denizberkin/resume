from pathlib import Path
from typing import Dict

from ..parsers.contact_parser import ContactParser
from ..parsers.section_parser import SectionParser
from ..parsers.skills_parser import SkillsParser
from ..builders.html_builder import HTMLBuilder
from .html_updater import HTMLUpdater


class ResumeConverter:
    """Main converter for LaTeX resume to HTML"""

    def __init__(self, base_dir: str = ".", verbose: bool = False):
        self.base_dir = Path(base_dir)
        self.verbose = verbose

        self.contact_parser = ContactParser(self.base_dir)
        self.section_parser = SectionParser(self.base_dir)
        self.skills_parser = SkillsParser(self.base_dir)

        self.html_builder = HTMLBuilder()
        self.html_updater = None

    def convert(self) -> bool:
        self._print_header()

        parsed_data = self._parse_all_sections()
        html_sections = self._build_html_sections(parsed_data)
        success = self._update_html_file(html_sections, parsed_data["contact"])

        return success

    def _parse_all_sections(self) -> Dict:
        """Parse all resume sections"""
        self._log("\nParsing contact information...")
        contact = self.contact_parser.parse()
        self._log(f"Name: {contact.get('name', 'N/A')}")
        self._log(f"Email: {contact.get('email', 'N/A')}")

        self._log("\nParsing work experience...")
        experience = self.section_parser.parse_file("experience.tex")
        self._log(f"Found {len(experience.get('subsections', []))} work experiences")

        self._log("\nParsing education...")
        education = self.section_parser.parse_file("education.tex")

        self._log("\nParsing projects/activities...")
        activities = self.section_parser.parse_file("activities.tex")
        self._log(f"Found {len(activities.get('subsections', []))} project sections")

        self._log("\nParsing skills...")
        skills = self.skills_parser.parse()
        self._log(f"Found {len(skills)} skill categories")

        return {
            "contact": contact,
            "experience": experience,
            "education": education,
            "activities": activities,
            "skills": skills,
        }

    def _build_html_sections(self, parsed_data: Dict) -> Dict[str, str]:
        """Build HTML for all sections"""
        self._log("\nBuilding HTML sections...")

        sections = {
            "work": self.html_builder.build_work_section(parsed_data["experience"]),
            "education": self.html_builder.build_education_section(parsed_data["education"]),
            "projects": self.html_builder.build_projects_section(parsed_data["activities"]),
            "skills": self.html_builder.build_skills_section(parsed_data["skills"]),
        }

        self._log("Work section built")
        self._log("Education section built")
        self._log("Projects section built")
        self._log("Skills section built")

        return sections

    def _update_html_file(self, html_sections: Dict[str, str], contact: Dict) -> bool:
        """Update HTML file with new content"""
        self._log("\nUpdating index.html...")

        html_path = self.base_dir / "index.html"

        if not html_path.exists():
            print(f"Error: {html_path} not found!")
            return False

        # Initialize updater
        self.html_updater = HTMLUpdater(html_path)

        # Validate structure
        if not self.html_updater.validate_structure():
            print("Warning: HTML structure validation failed")

        # Create backup
        if self.verbose:
            backup_success = self.html_updater.backup()
            if backup_success:
                self._log("Backup created")

        # Update sections
        sections_updated = 0
        for section_id, content in html_sections.items():
            if self.html_updater.update_section(section_id, content):
                sections_updated += 1
                self._log(f"Updated {section_id} section")
            else:
                self._log(f"Warning: Failed to update {section_id} section")

        # Update contact info
        self.html_updater.update_contact_info(contact)
        self._log("Updated contact information")

        # Save file
        if self.html_updater.save():
            self._log("\nSuccessfully updated index.html")
            self._log(f"File: {html_path}")
            self._log(f"Updated {sections_updated}/{len(html_sections)} sections")
            return True
        else:
            print("\nFailed to save HTML file")
            return False

    def _print_header(self):
        """Print header banner"""
        print("=" * 60)
        print("LaTeX to HTML Resume Converter")
        print("=" * 60)

    def _log(self, message: str):
        """Log message if verbose mode enabled"""
        if self.verbose or not message.startswith("   "):
            print(message)

    def get_statistics(self, parsed_data: Dict) -> Dict:
        return {
            "work_experiences": len(parsed_data["experience"].get("subsections", [])),
            "projects": len(parsed_data["activities"].get("subsections", [])),
            "skill_categories": len(parsed_data["skills"]),
            "total_skills": sum(len(skills) for skills in parsed_data["skills"].values()),
        }
