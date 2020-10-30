from loguru import logger

from .evadb_shared import require_login, EvaDBBase, Response
from .table_parser import extract_table, ParsingError


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

    @require_login
    def search(self, data: dict) -> Response:
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
        logger.debug("Query: {}", data)
        search_url = self._urls["search_call"]
        text = self._post_form(search_url, data)

        try:
            table_data = extract_table(text, "//*[@id=\"default\"]")
        except ParsingError as e:
            return Response(str(e), None)

        logger.debug("Found {} AD variants", len(table_data))
        return Response(None, table_data)

    @require_login
    def search_gene_ind(self, data: dict) -> Response:
        """Search AR variants.

        Example data dict: {
        }
        """
        logger.debug("Query: {}", data)
        gene_ind_url = self._urls["gene_ind_call"]
        text = self._post_form(gene_ind_url, data)

        try:
            table_data = extract_table(text, "(//html:table)[2]")
        except ParsingError as e:
            return Response(str(e), None)

        logger.debug("Found {} AR variants", len(table_data))
        return Response(None, table_data)

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
        logger.debug("Query: {}", data)
        sample_url = self._urls["search_sample_call"]
        text = self._post_form(sample_url, data)

        try:
            table_data = extract_table(text, "//*[@id=\"default\"]")
        except ParsingError as e:
            return Response(str(e), None)

        logger.debug("Found {} samples", len(table_data))
        return Response(None, table_data)
