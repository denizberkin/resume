"""
hardcode converting my resume format from .tex to html
"""

import os

from src.build.builder import BuildHTML
# from src.infer.inferer import Inference


os.environ["PROFILE_PICTURE_PATH"] = "assets/pp.gif"


def main():
    # add env variables to use in builders, deduct from .tex files
    resume_sections = {
        os.path.splitext(path)[0]: os.path.join("sections", path)
        for path in os.listdir("sections")
        if path.endswith(".tex")
    }
    resume_sections["resume"] = "resume.tex"
    # TODO: infer details and pass to builder/formatters

    html_template_dict = {
        os.path.splitext(path)[0]: os.path.join("src", "templates", path)
        for path in os.listdir("src/templates")
        if path.endswith(".html")
    }
    html = BuildHTML(html_template_dict).build()

    with open("generated.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()
