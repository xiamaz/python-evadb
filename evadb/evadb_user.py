from loguru import logger

from .evadb_shared import require_login, EvaDBBase, Response
from .table_parser import extract_table, ParsingError
from .csrf_parser import extract_csrf_tokens


class EvaDBUser(EvaDBBase):

    def set_session(self, session_id) -> "EvaDBUser":
        """Set a session id manually. This will set logged_in to true.
        """
        self._session.cookies["Exome"] = session_id
        self.logged_in = True
        return self

    def get_session(self) -> str:
        """Get current session id."""
        session_id = self._session.cookies.get("Exome")
        return session_id

    def _search_query(self, search_url, data, xpath, csrf_url=""):
        """Generic search query with csrf getting."""
        # get csrf for given call
        if csrf_url:
            csrf_text = self._session.get(csrf_url).text
            csrf_tokens = extract_csrf_tokens(csrf_text)
            data = {**data, **csrf_tokens}

        logger.debug("Query ({}): {}", search_url, data)
        text = self._post_form(search_url, data)

        try:
            table_data = extract_table(text, xpath)
            logger.debug("Successfully extracted table for query {} with {}", search_url, xpath)
        except ParsingError as e:
            logger.error("Failed to parse query {} with xpath {}.", search_url, xpath)
            return Response(str(e), None)

        return Response(None, table_data)

    @require_login
    def search_ad(self, data: dict) -> Response:
        """Search AD variants.

        Example data dict: {
            "ds.iddisease":  "312",
            "s.pedigree":    "S0001",
            "idproject":     "1",
            "x.alleles":     "1",
            "ncases":        "1",
            "npedigrees":    "1",
            "ncontrols":     "2",
            "avhet":         "",
            "aa_het":        "",
            "kaviar":        "",
            "affecteds":     "onlyaffecteds",
            "snvqual":       "",
            "gtqual":        "30",
            "mapqual":       "",
            "nonsynpergene": "1000",
            "length":        "",
            "lengthmax":     "",
            "class":         ["snp", "indel", "deletion"],
            "function":      ["unknown", "missense", "nonsense", "stoploss", "splice", "frameshift", "indel"],
            "showall":       "1",
            "printquery":    "no",
        }

        Returns:
            Response tuple consisting of error field and data field.
        """
        # get csrf for given call
        csrf_url = self._urls["search_ad_page"]
        search_url = self._urls["search_ad_call"]
        xpath = "//*[@id=\"results\"]"
        result = self._search_query(
            search_url=search_url,
            data=data,
            xpath=xpath,
            csrf_url=csrf_url
        )
        return result

    @require_login
    def search_ar(self, data: dict) -> Response:
        """Search AR variants.

        Example data dict: {
            "dg.iddisease":  "312",
            "ds.iddisease":  "",
            "s.name":        "S0002",
            "idproject":     "",
            "x.alleles":     "2",
            "v.idsnv":       "1",
            "ncontrols":     "15",
            "avhet":         "",
            "aa_het":        "",
            "kaviar":        "",
            "affecteds":     "all",
            "homozygous":    "0",
            "trio":          "0",
            "snvqual":       "",
            "gtqual":        "30",
            "mapqual":       "",
            "nonsynpergene": "1000",
            "length":        "",
            "lengthmax":     "",
            "class":         ["snp", "indel", "deletion"],
            "function":      ["unknown", "missense", "nonsense", "stoploss", "splice", "frameshift", "indel"],
            "printquery":    "no",
        }
        """
        csrf_url = self._urls["search_ar_page"]
        search_url = self._urls["search_ar_call"]
        xpath = "//*[@id=\"results\"]"
        result = self._search_query(
            search_url=search_url,
            data=data,
            xpath=xpath,
            csrf_url=csrf_url
        )
        return result

    @require_login
    def search_sample(self, data) -> Response:
        """Search all samples.

        Example data dict: {
            "datebegin":       "",
            "dateend":         "",
            "s.name":          "",
            "foreignid":       "",
            "pedigree":        "",
            "ds.iddisease":    "",
            "lstatus":         "",
            "s.idcooperation": "",
            "idproject":       "",
            "nottoseq":        "0"
        }
        """
        csrf_url = self._urls["search_sample_page"]
        search_url = self._urls["search_sample_call"]
        xpath = "//*[@id=\"default\"]"
        result = self._search_query(
            search_url=search_url,
            data=data,
            xpath=xpath,
            csrf_url=csrf_url
        )
        return result
