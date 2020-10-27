import pytest

from evadb import table_parser


SIMPLE_TABLE = (
    "<table><thead><tr><th>I<br><br></th><th>II</th><th>III<br></th></tr></thead><tbody><tr><td>a<br></td><td>b<br></td><td>c<br></td></tr></tbody></table>",
    [{"I": "a", "II": "b", "III": "c"}]
)
SIMPLE_TABLE_2_EMPTIES = (
    "<table><thead><tr><th>I<br><br></th><th>II</th><th>III<br></th></tr></thead><tbody><tr><td>a<br></td><td><br></td><td><br></td></tr></tbody></table>",
    [{"I": "a", "II": "", "III": ""}]
)
MULTI_TABLE = (
    "<table><thead><tr><th>I<br><br></th><th>II</th><th>III<br></th></tr></thead><tbody><tr><td>a<br></td><td>b<br></td><td>c<br></td></tr><tr><td>c</td><td>d</td><td>e</td></tr></tbody></table>",
    [{"I": "a", "II": "b", "III": "c"}, {"I": "c", "II": "d", "III": "e"}]
)
MULTI_TABLE_ROWMERGED = (
    "<table><thead><tr><th>I<br><br></th><th>II</th><th>III<br></th></tr></thead><tbody><tr><td>a<br></td><td rowspan=\"2\">b<br></td><td>c<br></td></tr><tr><td>c</td><td>e</td></tr></tbody></table>",
    [{"I": "a", "II": "b", "III": "c"}, {"I": "c", "II": "b", "III": "e"}]
)


def test_simple_table():
    """Check we can parse a simple table with a single data entry."""
    html, expected = SIMPLE_TABLE
    result = table_parser.extract_table(html, "//html:table")
    assert result == expected

def test_empty_values():
    html, expected = SIMPLE_TABLE_2_EMPTIES
    result = table_parser.extract_table(html, "//html:table")
    assert result == expected

def test_multi_values():
    html, expected = MULTI_TABLE
    result = table_parser.extract_table(html, "//html:table")
    assert result == expected

def test_multi_rowmerged():
    html, expected = MULTI_TABLE_ROWMERGED
    result = table_parser.extract_table(html, "//html:table")
    assert result == expected
