from obsidian2html import obsidian2html


def test_simple_text():
    actual = obsidian2html("Hello world")
    expected = "<p>Hello world</p>"
    assert expected == actual.strip()


def test_heading():
    actual = obsidian2html("## Subtitle")
    expected = "<h2>Subtitle</h2>"
    assert expected == actual.strip()


def test_internal_link():
    actual = obsidian2html("These are my [[Notes]]")
    expected = '<p>These are my <a href="Notes.html">Notes</a></p>'
    assert expected == actual.strip()


def test_internal_link_with_alt_text():
    actual = obsidian2html("Text with a [[target|link]]")
    expected = '<p>Text with a <a href="target.html">link</a></p>'
    assert expected == actual.strip()


def test_internal_non_markdown_link():
    actual = obsidian2html("Text with a [[target.png]]")
    expected = '<p>Text with a <a href="target.png">target.png</a></p>'
    assert expected == actual.strip()


def test_internal_non_markdown_link_with_alt_text():
    actual = obsidian2html("Text with a [[target.png|some image]]")
    expected = '<p>Text with a <a href="target.png">some image</a></p>'
    assert expected == actual.strip()


def test_external_link():
    actual = obsidian2html("Text with an [external link](http://example.com)")
    expected = '<p>Text with an <a href="http://example.com">external link</a></p>'
    assert expected == actual.strip()
