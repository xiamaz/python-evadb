from loguru import logger

import requests
import requests_cache

from .table_parser import extract_table

requests_cache.install_cache("evadb")


EVADB_URL = "https://ihg4.helmholtz-muenchen.de"
EVADB_LOGIN_URL = f"{EVADB_URL}/cgi-bin/mysql/snv-vcf/loginDo.pl"
EVADB_SEARCH_URL = f"{EVADB_URL}/cgi-bin/mysql/snv-vcf/searchDo.pl"
EVADB_SEARCH_SAMPLE_URL = f"{EVADB_URL}/cgi-bin/mysql/snv-vcf/searchSampleDo.pl"
EVADB_SEARCH_GENE_IND_URL = f"{EVADB_URL}/cgi-bin/mysql/snv-vcf/searchGeneIndDo.pl"


class UnauthorizedException(Exception):
    pass


def require_login(fn):
    """Enforce that a given function will only execute if properly logged in.

    Otherwise raise an unauthorized error.
    """
    def wrapped(self, *args, **kwargs):
        if not self.logged_in:
            raise UnauthorizedException()
        return fn(self, *args, **kwargs)
    return wrapped


def evadb_login(session: "Session", user: str, password: str) -> bool:
    """Log in as a user into evaDB snv-vcf."""
    data = {
        "name": user,
        "password": password,
        "yubikey": "",
    }

    resp = session.post(EVADB_LOGIN_URL, data=data)

    return resp.ok and "Login successful" in resp.text


class EvaDBUser:
    def __init__(self):
        self._session = requests.Session()
        self.logged_in = False

    def login(self, user: str, password: str) -> "EvaDBUser":
        """Login as the given user."""
        self.logged_in = evadb_login(self._session, user, password)
        if not self.logged_in:
            logger.error("Failed to login.")
        return self

    def _post_form(self, url, data):
        resp = self._session.post(url, data=data)
        resp.raise_for_status()
        return resp.text

    @require_login
    def search(self, data: dict) -> list:
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
        """
        text = self._post_form(EVADB_SEARCH_URL, data)
        table_data = extract_table(text, "//*[@id=\"default\"]")
        return table_data

    @require_login
    def search_gene_ind(self, data: dict) -> list:
        """Search AR variants.

        Example data dict: {
        }
        """
        text = self._post_form(EVADB_SEARCH_GENE_IND_URL, data)
        table_data = extract_table(text, "(//html:table)[2]")
        return table_data

    @require_login
    def search_sample(self, data) -> list:
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
        text = self._post_form(EVADB_SEARCH_SAMPLE_URL, data)
        table_data = extract_table(text, "//*[@id=\"default\"]")
        return table_data
