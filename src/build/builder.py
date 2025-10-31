from src.build import BuildHeader, BuildSidebar, BuildBody, BuildMainContent, BuildScript


class BuildHTML:
    def __init__(self, template_paths: dict):
        self.template_paths = template_paths

    def build(self, **kwargs) -> str:
        # create builders

        bsidebar = BuildSidebar(self.template_paths.get("sidebar"), indent_level=2, **kwargs)
        bmain = BuildMainContent(self.template_paths, indent_level=2, **kwargs)
        bscript = BuildScript(self.template_paths.get("script"), indent_level=1, **kwargs)

        bheader = BuildHeader(self.template_paths.get("header"), indent_level=0, **kwargs)
        bbody = BuildBody(self.template_paths.get("body"), indent_level=0, **kwargs)

        # build
        sidebar = bsidebar.build()
        main_content = bmain.build()
        script = bscript.build()

        header = bheader.build()
        body = bbody.build(sidebar=sidebar, main_content=main_content, script=script)

        # Load main template
        with open(self.template_paths.get("combined"), "r", encoding="utf-8") as f:
            main_template = f.read()

        final_html = self.format(main_template, header=header, body=body)

        return final_html

    def format(self, html: str, header: str, body: str) -> str:
        """any formatting necessary"""
        return html.replace("{HEADER}", header).replace("{BODY}", body)
