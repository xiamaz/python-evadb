from loguru import logger

from .evadb_shared import require_login, EvaDBBase
from .table_parser import extract_table


def evadb_login(session: "Session", url: str, user: str, password: str, csrf: str = "", wwwcsrf: str = "") -> bool:
    """Log in as a user into evaDB snv-vcf."""
    data = {
        "name": user,
        "password": password,
        "yubikey": "",
        "csrf": csrf,
        "wwwcsrf": wwwcsrf,
    }
    resp = session.post(url, data=data)

    return resp.ok and "Login successful" in resp.text


class EvaDBUser(EvaDBBase):
    def login(self, user: str, password: str) -> "EvaDBUser":
        """Login as the given user."""
        csrf_tokens = self._obtain_csrf_token()
        login_url = self._urls["login_call"]

        self.logged_in = evadb_login(
            self._session,
            login_url,
            user,
            password,
            csrf=csrf_tokens["csrf"],
            wwwcsrf=csrf_tokens["wwwcsrf"])

        if not self.logged_in:
            logger.error("Failed to login.")
        else:
            logger.info("Successfully logged in.")
        return self

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
        search_url = self._urls["search_call"]
        text = self._post_form(search_url, data)
        table_data = extract_table(text, "//*[@id=\"default\"]")
        return table_data

    @require_login
    def search_gene_ind(self, data: dict) -> list:
        """Search AR variants.

        Example data dict: {
        }
        """
        gene_ind_url = self._urls["gene_ind_call"]
        text = self._post_form(gene_ind_url, data)
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
        sample_url = self._urls["search_sample_call"]
        text = self._post_form(sample_url, data)
        table_data = extract_table(text, "//*[@id=\"default\"]")
        return table_data
