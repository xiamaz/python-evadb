import requests

U = "http://localhost:5000"
S = requests.Session()

resp = S.get(U)
print(resp.json())

resp = S.post(U + "/login", json={"user": "TestUser1", "password": "TestUser1"})
resp = S.post(U + "/next/getPatient", json={"id": "205"})

req = requests.Request("POST", url=U+"/legacy/samples", json={})

p = S.prepare_request(req)
S.send(p)
c = list(S.cookies)[0]
c.domain = ''
c.secure = False
S.cookies.set("session", "7c46b1fb-f98f-44d4-a3cf-1b5929f6d918")

resp = S.post(U + "/legacy/samples", json={}, cookies={"just": "checkin"})

resp = S.post(U + "/legacy/search-ar", json={
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

resp.json()
S.cookies
