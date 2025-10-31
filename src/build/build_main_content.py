import os
from src.utils import append_indentation

from src.build import BuildWorkExperiences


class BuildMainContent:
    def __init__(self, template_paths: dict, indent_level: int = 0, **kwargs):
        self.template_path = template_paths.get("main_content")
        self.experiences_builder = BuildWorkExperiences(
            template_paths.get("single_experience"), indent_level=indent_level + 2, **kwargs
        )

        self.indent_level = indent_level
        self.spaces = " " * (self.indent_level * 4)
        self.kwargs = kwargs

    def build(self) -> str:
        with open(self.template_path, "r+", encoding="utf-8") as f:
            template = f.read()
        experiences = self.experiences_builder.build()
        html = self.format(template, experiences)
        return append_indentation(html, self.spaces)

    def format(self, html: str, experiences: list[str]) -> str:
        """TODO: add"""
        """
        add_section_to_basics format:
        \t\t\t<div class="basics-label">Section Title</div>
        \t\t\t<div>Section Information</div>
        """
        # id:basics, class:basics-card: [NAME, TITLE, EMAIL, LOCATION, LINKEDIN, GITHUB, ADD_SECTION_TO_BASICS]
        # id:work, class:section, []
        for key, value in self.kwargs.items():
            value = "" if value is None else value
            v = value or os.getenv(key.upper(), "")
            key = "{" + key.upper() + "}"
            html = html.replace(key, v)
        return html
