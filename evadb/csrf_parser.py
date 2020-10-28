from loguru import logger

from lxml import html
import html5lib


def extract_csrf_tokens(text):
    csrf_tokens = {
        "csrf": "",
        "wwwcsrf": "",
    }
    tree = html5lib.parse(text, treebuilder="lxml")
    nss = tree.getroot().nsmap

    csrf_elem = tree.xpath("//html:input[@name=\"csrf\"]", namespaces=nss)
    if csrf_elem:
        csrf_tokens["csrf"] = csrf_elem[0].get("value")
        logger.debug("Found csrf with value: {}", csrf_tokens["csrf"])

    wwwcsrf_elem = tree.xpath("//html:input[@name=\"wwwcsrf\"]", namespaces=nss)
    if wwwcsrf_elem:
        csrf_tokens["wwwcsrf"] = wwwcsrf_elem[0].get("value")
        logger.debug("Found wwwcsrf with value: {}", csrf_tokens["wwwcsrf"])

    return csrf_tokens
