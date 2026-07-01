"""Markdown viewer widget using Qt WebEngine."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QMenuBar, QMenu, QFileDialog,
    QToolBar, QMessageBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QFileSystemWatcher, QSettings, Slot
from PySide6.QtGui import QAction

from .renderer import MarkdownRenderer


class MarkdownViewer(QMainWindow):
    """Main window for viewing Markdown files."""

    def __init__(self) -> None:
        super().__init__()
        self._current_file: Optional[Path] = None
        self._dark_mode: bool = False
        self._renderer = MarkdownRenderer()
        self._watcher = QFileSystemWatcher()

        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()
        self._connect_signals()
        self._load_settings()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("mdreader")
        self.resize(900, 700)

        self._web_view = QWebEngineView()
        self._web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )
        self.setCentralWidget(self._web_view)

        # Show empty state
        self._show_welcome()

    def _setup_menu(self) -> None:
        """Set up the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file_dialog)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        self._dark_action = QAction("Dark Mode", self, checkable=True)
        self._dark_action.setShortcut("Ctrl+D")
        self._dark_action.triggered.connect(self._toggle_dark_mode)
        view_menu.addAction(self._dark_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_toolbar(self) -> None:
        """Set up the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self._open_file_dialog)
        toolbar.addAction(open_action)

    def _connect_signals(self) -> None:
        """Connect signals."""
        self._watcher.fileChanged.connect(self._on_file_changed)

    def _load_settings(self) -> None:
        """Load saved settings."""
        settings = QSettings("mdreader", "mdreader")
        self._dark_mode = settings.value("dark_mode", False, type=bool)
        self._dark_action.setChecked(self._dark_mode)

    def _save_settings(self) -> None:
        """Save current settings."""
        settings = QSettings("mdreader", "mdreader")
        settings.setValue("dark_mode", self._dark_mode)

    def _show_welcome(self) -> None:
        """Show welcome message."""
        html = """
        <div style="text-align: center; padding: 50px;">
            <h1>mdreader</h1>
            <p>A lightweight Markdown viewer with LaTeX support</p>
            <p>Press <strong>Ctrl+O</strong> or click <strong>Open</strong> to open a file.</p>
        </div>
        """
        self._web_view.setHtml(html)

    def load_file(self, path: Path) -> None:
        """Load a Markdown file."""
        if not path.exists():
            QMessageBox.warning(
                self, "Error",
                f"File not found: {path}"
            )
            return

        self._current_file = path

        # Update watcher
        if self._watcher.files():
            self._watcher.removePaths(self._watcher.files())
        self._watcher.addPath(str(path))

        self._render_file()
        self.setWindowTitle(f"mdreader - {path.name}")

    def _render_file(self) -> None:
        """Render the current file."""
        if not self._current_file:
            return

        try:
            content = self._current_file.read_text(encoding="utf-8")
            base_path = self._current_file.parent.resolve()
            html = self._renderer.render(
                content,
                dark_mode=self._dark_mode,
                base_path=base_path
            )
            self._web_view.setHtml(
                html,
                baseUrl=base_path.as_uri() + "/"
            )
        except Exception as e:
            QMessageBox.warning(
                self, "Error",
                f"Failed to render file: {e}"
            )

    @Slot()
    def _open_file_dialog(self) -> None:
        """Open file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        if file_path:
            self.load_file(Path(file_path))

    @Slot()
    def _toggle_dark_mode(self) -> None:
        """Toggle dark mode."""
        self._dark_mode = self._dark_action.isChecked()
        self._save_settings()
        self._render_file()

    @Slot(str)
    def _on_file_changed(self, path: str) -> None:
        """Handle file changes for live reload."""
        if self._current_file and str(self._current_file) == path:
            self._render_file()

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About mdreader",
            "mdreader v0.1.0\n\n"
            "A lightweight Markdown viewer with LaTeX equation rendering.\n\n"
            "Licensed under MIT License."
        )

    def closeEvent(self, event) -> None:  # type: ignore
        """Handle window close."""
        self._save_settings()
        event.accept()