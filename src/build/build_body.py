from src.utils import append_indentation


class BuildBody:
    def __init__(self, template_path: str, indent_level: int = 0, **kwargs):
        self.template_path = template_path
        self.indent_level = indent_level
        self.spaces = " " * (self.indent_level * 4)
        self.kwargs = kwargs

    def build(self, sidebar: str, main_content: str, script: str) -> str:
        with open(self.template_path, "r+", encoding="utf-8") as f:
            template = f.read()
        html = self.format(template, sidebar, main_content, script)
        return append_indentation(html, self.spaces)

    def format(self, html: str, sidebar: str, main_content: str, script: str) -> str:
        """any formatting necessary"""
        html = html.replace("{SIDEBAR}", sidebar)
        html = html.replace("{MAIN_CONTENT}", main_content)
        html = html.replace("{SCRIPT}", script)
        return html
