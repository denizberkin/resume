from typing import Dict


class IconMapper:
    """Map skills to appropriate Font Awesome icons"""

    # Icon mapping: keyword -> Font Awesome class
    SKILL_ICONS: Dict[str, str] = {
        # Programming Languages
        "python": "fab fa-python",
        "java": "fab fa-java",
        "javascript": "fab fa-js",
        "c++": "fas fa-code",
        "c &": "fas fa-code",
        "c ": "fas fa-code",
        "matlab": "fas fa-calculator",
        "sql": "fas fa-table",
        "r ": "fas fa-chart-bar",
        # Frameworks & Libraries
        "pytorch": "fas fa-fire",
        "tensorflow": "fas fa-project-diagram",
        "tf ": "fas fa-project-diagram",
        "keras": "fas fa-project-diagram",
        "opencv": "fas fa-eye",
        "react": "fab fa-react",
        "vue": "fab fa-vuejs",
        "angular": "fab fa-angular",
        # Tools & Platforms
        "git": "fab fa-git-alt",
        "docker": "fab fa-docker",
        "kubernetes": "fas fa-dharmachakra",
        "aws": "fab fa-aws",
        "azure": "fab fa-microsoft",
        "mongodb": "fas fa-database",
        "postgresql": "fas fa-database",
        "redis": "fas fa-database",
        "cuda": "fas fa-microchip",
        "mlflow": "fas fa-project-diagram",
        "jupyter": "fas fa-book",
        # Web Technologies
        "html": "fab fa-html5",
        "css": "fab fa-css3-alt",
        "node": "fab fa-node",
        "npm": "fab fa-npm",
        # Categories
        "medical": "fas fa-microscope",
        "scene": "fas fa-film",
        "mathematical": "fas fa-chart-line",
        "visualization": "fas fa-chart-pie",
        "processing": "fas fa-microchip",
        "segmentation": "fas fa-cut",
        # Languages
        "turkish": "fas fa-flag",
        "english": "fas fa-flag",
        "german": "fas fa-flag",
        "french": "fas fa-flag",
        "spanish": "fas fa-flag",
        "chinese": "fas fa-flag",
        "japanese": "fas fa-flag",
    }
    DEFAULT_ICON = "fas fa-check"

    def get_icon(self, skill: str) -> str:
        skill_lower = skill.lower()

        # check for keyword matches
        for keyword, icon_class in self.SKILL_ICONS.items():
            if keyword in skill_lower:
                return f'<i class="{icon_class}"></i>'

        # return default icon if no match found
        return f'<i class="{self.DEFAULT_ICON}"></i>'

    def add_custom_mapping(self, keyword: str, icon_class: str) -> None:
        self.SKILL_ICONS[keyword.lower()] = icon_class

    def get_available_icons(self) -> Dict[str, str]:
        """Get dictionary of all available icon mappings"""
        return self.SKILL_ICONS.copy()
