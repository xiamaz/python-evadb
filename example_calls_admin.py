import requests_cache
from evadb.evadb_admin import EvaDBAdmin

# requests_cache.install_cache()

EVADB_USER_HOST = "https://localhost:8443/cgi-bin"

print("Doing a test run")
eva = EvaDBAdmin(EVADB_USER_HOST, "", "")
eva._session.verify = False
eva.login("admin", "admin_pw")
