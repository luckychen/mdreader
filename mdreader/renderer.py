"""Markdown to HTML renderer with MathJax, Mermaid, SVG, and syntax highlighting."""

from pathlib import Path
from typing import Optional

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin


def _render_math_inline(slf, tokens, idx, options, env):
    # Output \(...\) so MathJax finds it regardless of surrounding markdown
    return "\\(" + tokens[idx].content + "\\)"


def _render_math_block(slf, tokens, idx, options, env):
    return '<div class="math-display">\\[\n' + tokens[idx].content + "\n\\]</div>\n"


class MarkdownRenderer:
    """Renders Markdown to HTML with MathJax, Mermaid, SVG, and syntax highlighting."""

    def __init__(self) -> None:
        self._md = MarkdownIt("gfm-like", {"html": True, "linkify": False})
        dollarmath_plugin(self._md)
        self._md.add_render_rule("math_inline", _render_math_inline)
        self._md.add_render_rule("math_block", _render_math_block)
        self._template_path = Path(__file__).parent / "resources" / "template.html"

    def render(
        self,
        markdown: str,
        dark_mode: bool = False,
        base_path: Optional[Path] = None,
    ) -> str:
        """Render Markdown to HTML.

        Args:
            markdown: Markdown content to render.
            dark_mode: Whether to use dark theme.
            base_path: Base path for resolving relative links.

        Returns:
            HTML string with MathJax, Mermaid, and syntax highlighting support.
        """
        html_content = self._md.render(markdown)

        template = self._template_path.read_text(encoding="utf-8")

        theme = "dark" if dark_mode else "light"
        hljs_theme = "github-dark" if dark_mode else "github"
        html = template.replace("{{ theme }}", theme)
        html = html.replace("{{ hljs_theme }}", hljs_theme)
        html = html.replace("{{ content }}", html_content)

        return html
