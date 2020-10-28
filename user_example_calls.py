import requests_cache
from evadb.evadb_user import EvaDBUser

# requests_cache.install_cache()

EVADB_USER_HOST = "https://localhost:443/cgi-bin"

print("Doing a test run")
# eva = EvaDBUser(EVADB_USER_HOST, "", "")
eva = EvaDBUser()
eva._session.verify = False
eva.login("TestUser1", "TestUser1")
# eva.login("admin", "admin_pw")

print("Searching normal AD variants")
variants = eva.search({
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
})

print("Searching samples")
samples = eva.search_sample({
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
})

print("Searching normal AR variants")
ar_variants = eva.search_gene_ind({
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
})

print(f"Found {len(samples)} samples, {len(variants)} variants, {len(ar_variants)} ar-variants")
