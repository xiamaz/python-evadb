from loguru import logger

import requests

from .evadb_shared import EvaDBBase
from .evadb_urlbuilder import build_evadb_urls
from .table_parser import extract_table
from .csrf_parser import extract_csrf_tokens


class EvaDBAdmin(EvaDBBase):
    pass
