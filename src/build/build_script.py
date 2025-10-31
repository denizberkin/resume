from ..utils import append_indentation


class BuildScript:
    def __init__(self, template_path: str, indent_level: int = 0, **kwargs):
        self.template_path = template_path
        self.indent_level = indent_level
        self.spaces = " " * (self.indent_level * 4)
        self.kwargs = kwargs

    def build(self) -> str:
        with open(self.template_path, "r+", encoding="utf-8") as f:
            template = f.read()
        html = self.format(template)
        return append_indentation(html, self.spaces)

    def format(self, html: str) -> str:
        """any formatting necessary"""
        return html
