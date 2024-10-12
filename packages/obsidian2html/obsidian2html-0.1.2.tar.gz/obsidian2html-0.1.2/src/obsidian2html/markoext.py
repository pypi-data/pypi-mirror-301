import html
from os.path import basename, splitext
from re import Match
from typing import Any, Callable

from marko import inline
from marko.helpers import MarkoExtension


def no_ext(filename: str) -> bool:
    _, ext = splitext(filename)
    return ext == ""


class InternalLink(inline.InlineElement):
    pattern: str = r"\[\[ *(.+?) *(\| *(.+?) *)?\]\]"

    parse_children: bool = True
    parse_group: int = 3

    def __init__(self, match: Match[str]) -> None:

        link_text = None
        target = match.group(1)

        # If there's no text group, the target is the link text
        if match.group(3) is None:
            link_text = match.group(1)

        # If the target has no extension, assume it's markdown and append .html to target the processed file
        if no_ext(target):
            target = f"{target}.html"

        self.target = target 
        self.link_text = link_text



class InternalLinkRenderer(object):
    """ """

    escape_url: Callable[[str], str]
    render_children: Callable[[Any], str]

    def render_internal_link(self, element: Any) -> str:

        if element.link_text:
            return '<a href="{}">{}</a>'.format(
                self.escape_url(element.target), html.escape(element.link_text)
            )

        return '<a href="{}">{}</a>'.format(
            self.escape_url(element.target), self.render_children(element)
        )


Obsidian = MarkoExtension(
    elements=[InternalLink], renderer_mixins=[InternalLinkRenderer]
)
