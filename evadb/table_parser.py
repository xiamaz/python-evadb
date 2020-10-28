import html5lib


class ParsingError(Exception):
    pass


def _clean_text(node):
    text = " ".join(node.itertext()).strip()
    return text


def _extract_table_entries(table_body, colnames):
    rowspans = [{"count": 0, "value": ""} for _ in colnames]
    entries = []
    for row in table_body:
        row_values = []
        row_iter = iter(row)
        for i, rowspan in enumerate(rowspans):

            if rowspan["count"] > 0:
                value = rowspan["value"]
            else:
                elem = next(row_iter)
                elem_rowspan = elem.get("rowspan")
                value = _clean_text(elem)
                if elem_rowspan:
                    rowspans[i]["count"] = int(elem_rowspan)
                    rowspans[i]["value"] = value

            row_values.append(value)
            rowspans[i]["count"] -= 1

        entries.append(dict(zip(colnames, row_values)))
    return entries


def extract_table(text: str, table_xpath: str) -> list:
    """Extract a html table from the given data.

    Args:
        text: entire HTML document
        table_xpath: XPath selector for a given table.

    Returns:
        List of dicts containing each row as a dict with column names as keys.
    """
    tree = html5lib.parse(text, treebuilder="lxml")
    nss = tree.getroot().nsmap

    # try to find a table in the given page
    try:
        table = tree.xpath(table_xpath, namespaces=nss)[0]
    except IndexError as e:
        raise ParsingError(f"Cannot find table. :::XPath: {table_xpath}:::HTML: {text}") from e

    thead, tbody = table
    colnames = [_clean_text(t) for t in thead[0]]
    entries = _extract_table_entries(tbody, colnames)
    return entries
