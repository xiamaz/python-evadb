from loguru import logger

from .evadb_shared import require_login, EvaDBBase, Response
from .constants import EVADB_USER_HOST
from .table_parser import extract_table, ParsingError
from .csrf_parser import extract_csrf_tokens


SESSION_CHECK_NEEDLE = {
    "search_sample_page": '<meta http-equiv="refresh" content="0; URL=login.pl">'
}


class EvaDBUser(EvaDBBase):

    pages = {
        "login_page": "/login.pl",
        "login_call": "/loginDo.pl",
        "search_ad_page": "/search.pl",
        "search_ad_call": "/searchDo.pl",
        "search_ar_page": "/searchGeneInd.pl",
        "search_ar_call": "/searchGeneIndDo.pl",
        "search_sample_page": "/searchStat.pl",
        "search_sample_call": "/searchSampleDo.pl",
        "show_hpo_page": "/showHPO.pl",
    }

    def __init__(self, host=EVADB_USER_HOST):
        super().__init__(host)

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

    def check_session(self) -> bool:
        """Test if the current session is still logged in."""
        for page_key, needle in SESSION_CHECK_NEEDLE.items():
            result = self._session.get(self._urls[page_key])
            text = result.text

            # stop if logged-out indicator found
            if needle in text:
                self.logged_in = False
                break
        else:
            # logged in is true if all tests are normal
            self.logged_in = True

        return self.logged_in

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

    def _search_page(self, search_url, params, xpath):
        logger.debug("Get Page ({}): {}", search_url, params)
        response = self._session.get(search_url, params=params)
        text = response.text

        try:
            table_data = extract_table(text, xpath)
            logger.debug("Successfully extracted table for get-request {} with {}", search_url, xpath)
        except ParsingError as e:
            logger.error("Failed to parse get {} with xpath {}.", search_url, xpath)
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
        data["showall"] = "1"

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
        data["showall"] = "1"

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

    @require_login
    def show_hpo(self, idsample) -> Response:
        """Show list of HPO terms."""
        page_url = self._urls["show_hpo_page"]
        result = self._search_page(
            page_url,
            {"idsample": idsample},
            "//*[@id=\"default\"]"
        )
        return result
