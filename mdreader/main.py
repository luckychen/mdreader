"""Main entry point for mdreader."""

import sys
import argparse
from pathlib import Path

from PySide6.QtWidgets import QApplication
from .viewer import MarkdownViewer


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="mdreader",
        description="Lightweight Markdown viewer with LaTeX support"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Markdown file to open"
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setApplicationName("mdreader")

    viewer = MarkdownViewer()

    if args.file:
        path = Path(args.file).resolve()
        if path.exists():
            viewer.load_file(path)
        else:
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

    viewer.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()