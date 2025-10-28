from typing import Dict, List

from .icon_mapper import IconMapper


class HTMLBuilder:
    """Build HTML for resume sections"""

    def __init__(self):
        """Initialize HTML builder with icon mapper"""
        self.icon_mapper = IconMapper()

    def build_work_section(self, experience_data: Dict) -> str:
        html_parts = []

        for subsection in experience_data.get("subsections", []):
            html = self._build_work_item(
                subsection["title"], subsection["date"], subsection["subtext"], subsection["items"]
            )
            html_parts.append(html)

        return "\n                \n".join(html_parts)

    def _build_work_item(self, title: str, date: str, company: str, items: List[str]) -> str:
        """Build HTML for a single work experience item"""
        html = f"""
                <div class="work-item">
                    <div class="work-header">
                        <div class="work-title">{title}</div>
                        <div class="work-date">{date}</div>
                    </div>
                    <div class="work-company">
                        <i class="fas fa-building"></i>
                        {company}
                    </div>
                    <div class="work-details">
                        <ul>
            """

        for item in items:
            html += f"                            <li>{item}</li>\n"

        html += """                        </ul>
                    </div>
                </div>
            """
        return html.strip()

    def build_education_section(self, education_data: Dict) -> str:
        content = education_data.get("direct_content", "Education information not available")

        return f"""<div class="education-item">
                    <div class="edu-header">
                        <div class="edu-title">{content}</div>
                    </div>
                </div>"""

    def build_projects_section(self, activities_data: Dict) -> str:
        html_parts = []

        for subsection in activities_data.get("subsections", []):
            html = self._build_project_item(subsection["title"], subsection["items"])
            html_parts.append(html)

        return "\n                \n".join(html_parts)

    def _build_project_item(self, title: str, items: List[str]) -> str:
        """Build HTML for a single project item"""
        html = f"""
                <div class="project-item">
                    <h3>{title}</h3>
                    <div class="project-details">
                        <ul>
"""

        for item in items:
            html += f"                            <li>{item}</li>\n"

        html += """                        </ul>
                    </div>
                </div>
"""
        return html.strip()

    def build_skills_section(self, skills_data: Dict[str, List[str]]) -> str:
        html_parts = []

        for category, items in skills_data.items():
            html = self._build_skill_category(category, items)
            html_parts.append(html)

        return "\n\n".join(html_parts).rstrip()

    def _build_skill_category(self, category: str, items: List[str]) -> str:
        """Build HTML for a single skill category"""
        html = f'                    <div class="skill-category">{category}</div>\n'
        html += '                    <div class="skill-items">\n'

        for item in items:
            icon = self.icon_mapper.get_icon(item)
            html += f'                        <span class="skill-item">{icon} {item}</span>\n'

        html += "                    </div>"

        return html

    def build_languages_section(self, languages: List[str]) -> str:
        html = '                    <div class="skill-category">Communication</div>\n'
        html += '                    <div class="skill-items">\n'

        for lang in languages:
            icon = self.icon_mapper.get_icon(lang)
            html += f'                        <span class="skill-item">{icon} {lang}</span>\n'

        html += "                    </div>"

        return html
