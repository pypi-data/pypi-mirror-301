from marko import Markdown

from .markoext import Obsidian


def obsidian2html(md: str) -> str:
    markdown = Markdown(extensions=["codehilite", Obsidian])
    return markdown(md)
