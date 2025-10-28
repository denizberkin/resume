import sys
import argparse
from pathlib import Path

from src.core.converter import ResumeConverter


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Convert LaTeX resume files to HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\nExamples:\npython latex2html.py\npython latex2html.py --base-dir /path/to/resume""",
    )

    parser.add_argument(
        "--base-dir", type=str, default=".", help="Base directory containing resume files (default: current directory)"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()

    # Validate base directory
    base_dir = Path(args.base_dir)
    if not base_dir.exists():
        print(f"Error: Directory '{base_dir}' does not exist")
        sys.exit(1)

    # Check for required files - look for main LaTeX file
    main_tex_files = ["resume.tex", "main.tex", "cv.tex"]
    main_tex_found = any((base_dir / f).exists() for f in main_tex_files)

    if not main_tex_found:
        print(f"Warning: No main LaTeX file found ({', '.join(main_tex_files)})")
        print("Proceeding anyway...\n")

    # Check for index.html
    if not (base_dir / "index.html").exists():
        print("Warning: index.html not found")
        print("Proceeding anyway...\n")

    # Check for sections directory
    if not (base_dir / "sections").exists():
        print("Warning: sections/ directory not found")
        print("This may cause parsing to fail.\n")

    # Run conversion
    try:
        converter = ResumeConverter(base_dir=str(base_dir), verbose=args.verbose)
        converter.convert()

        print("\nConversion completed successfully!")
        return 0

    except Exception as e:
        print(f"\nError during conversion: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
