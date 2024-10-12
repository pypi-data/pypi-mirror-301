# obsidian2html

Convert Obsidian-flavoured markdown to HTML.

## Installation

```
pip install obsidian2html
```

## Usage

On the command line:

```
obsidian2html infile outfile
```

As a python library:

```python
from obsidian2html import obsidian2html

src = '''
# A simple markdown file

Hello world!
'''

html: str = obsidian2html(src)

print(html)
```

## Features

 - Convert internal links:
   ```
   [[my notes|Notes]] -> <a href="Notes.html">my notes</a>
   [[a non-obsidian-markdown link|example.pdf]] -> <a href="example.pdf">a non-obsidian-markdown link</a>

   ```

## Missing features

Basics:

 - Support for checklists - https://codepen.io/ouroboros8/pen/KKOzmBX
 - comments `%%this is an obsidian markdown inline comment%%`
 - footnotes

Advanced:

 - callouts
 - MathJAX
 - Tables
 - mermaid diagrams

## References

 - [Obsidian's basic formatting syntax](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax)
 - [Obsidian Flavoured Markdown](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown)
