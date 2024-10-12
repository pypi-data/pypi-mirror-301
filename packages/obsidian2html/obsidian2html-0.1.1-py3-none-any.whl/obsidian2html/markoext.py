from os.path import splitext
from re import Match
from typing import Any, Callable

from marko import inline
from marko.helpers import MarkoExtension


def has_ext(filename: str) -> bool:
    _, ext = splitext(filename)
    return ext != ""


class InternalLink(inline.InlineElement):
    pattern: str = r"\[\[ *(.+?) *\| *(.+?) *\]\]"

    parse_children: bool = True
    parse_group: int = 2

    def __init__(self, match: Match[str]) -> None:
        target = match.group(1)
        if not has_ext(target):
            target = f"{target}.html"

        self.target = target


class InternalLinkRenderer(object):
    """ """

    escape_url: Callable[[str], str]
    render_children: Callable[[Any], str]

    def render_internal_link(self, element: Any) -> str:
        return '<a href="{}">{}</a>'.format(
            self.escape_url(element.target), self.render_children(element)
        )


Obsidian = MarkoExtension(
    elements=[InternalLink], renderer_mixins=[InternalLinkRenderer]
)
