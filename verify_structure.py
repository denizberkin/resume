from pathlib import Path
import sys


def check_structure():
    """Check and display the repository structure"""
    print("=" * 60)
    print("Resume Repository Structure Checker")
    print("=" * 60)
    print()

    base_dir = Path(".")
    issues = []
    warnings = []

    # Check for main LaTeX file
    print("Checking main LaTeX file...")
    main_tex_files = ["resume.tex", "main.tex", "cv.tex"]
    main_tex_found = None

    for name in main_tex_files:
        if (base_dir / name).exists():
            main_tex_found = name
            print(f"Found: {name}")
            break

    if not main_tex_found:
        issues.append("No main LaTeX file found (resume.tex, main.tex, or cv.tex)")
        print(f"Not found: {', '.join(main_tex_files)}")

    # Check for sections directory
    print("Checking sections directory...")
    sections_dir = base_dir / "sections"

    if sections_dir.exists() and sections_dir.is_dir():
        print("Found: sections/")

        # Check for section files
        section_files = ["experience.tex", "education.tex", "activities.tex", "skills.tex"]
        print("Section files:")

        for section_file in section_files:
            section_path = sections_dir / section_file
            if section_path.exists():
                print(f"{section_file}")
            else:
                warnings.append(f"Section file not found: sections/{section_file}")
                print(f"{section_file} (not found)")
    else:
        issues.append("sections/ directory not found")
        print("Not found: sections/")

    print()

    # Check for HTML file
    print("Checking HTML file...")
    if (base_dir / "index.html").exists():
        print("Found: index.html")
    else:
        warnings.append("index.html not found")
        print("Not found: index.html")

    print()

    # Check for converter files
    print("Checking converter installation...")
    converter_files = [
        "latex2html.py",
        "src/__init__.py",
        "src/parsers/__init__.py",
        "src/parsers/latex_cleaner.py",
        "src/parsers/contact_parser.py",
        "src/parsers/section_parser.py",
        "src/parsers/skills_parser.py",
        "src/builders/__init__.py",
        "src/builders/icon_mapper.py",
        "src/builders/html_builder.py",
        "src/core/__init__.py",
        "src/core/html_updater.py",
        "src/core/converter.py",
    ]

    missing_converter_files = []
    for file in converter_files:
        file_path = base_dir / file
        if not file_path.exists():
            missing_converter_files.append(file)

    if missing_converter_files:
        print(f"Missing {len(missing_converter_files)} converter files:")
        for file in missing_converter_files[:5]:  # Show first 5
            print(f"{file}")
        if len(missing_converter_files) > 5:
            print(f"      ... and {len(missing_converter_files) - 5} more")
    else:
        print("All converter files present")

    print()

    # Display current structure
    print("Current structure:")
    print()

    def print_tree(directory, prefix="", max_depth=2, current_depth=0):
        """Print directory tree"""
        if current_depth >= max_depth:
            return

        try:
            items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            items = [x for x in items if not x.name.startswith(".") and x.name != "__pycache__"]

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")

                if item.is_dir():
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(item, next_prefix, max_depth, current_depth + 1)
        except PermissionError:
            pass

    print_tree(base_dir)

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    # Display issues
    if issues:
        print("\nCritical Issues:")
        for issue in issues:
            print(f" - {issue}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f" - {warning}")

    if not issues and not warnings:
        print("\nAll checks passed! Your repository structure is correct.")
        print("\nYou can run:")
        print("   python latex2html.py --verbose")
    elif not issues:
        print("\nNo critical issues found.")
        print("Some optional files are missing, but conversion should work.")
        print("\nYou can run:")
        print("   python latex2html.py --verbose")
    else:
        print("\nPlease fix the critical issues above before running the converter.")

    print()

    # Show detected configuration
    print("=" * 60)
    print("Detected Configuration")
    print("=" * 60)
    print(f"Main LaTeX file: {main_tex_found or 'NOT FOUND'}")
    print(f"Sections directory: {'sections/' if sections_dir.exists() else 'NOT FOUND'}")
    print(f"HTML file: {'index.html' if (base_dir / 'index.html').exists() else 'NOT FOUND'}")
    print(f"Converter: {'Installed' if not missing_converter_files else 'NOT INSTALLED'}")
    print("=" * 60)

    return len(issues) == 0


if __name__ == "__main__":
    success = check_structure()
    sys.exit(0 if success else 1)
