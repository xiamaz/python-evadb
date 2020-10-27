import os
import urllib

import pytest

import requests
from evadb import evadb_user

HERE = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture
def login_mock(requests_mock):
    with open(os.path.join(HERE, "data/login_fail.html"), "r") as f:
        login_fail = f.read()
    with open(os.path.join(HERE, "./data/login_success.html"), "r") as f:
        login_succ = f.read()

    def text_callback(request, context):
        req_data = urllib.parse.parse_qs(request.text)
        user = req_data["name"][0]
        password = req_data["password"][0]

        if user == "admin" and password == "admin_pw":
            return login_succ

        return login_fail

    requests_mock.post(evadb_user.EVADB_LOGIN_URL, text=text_callback)


def test_evadb_login_wrong(login_mock):
    eva = evadb_user.EvaDBUser()
    eva = eva.login("TestUser1", "TestUser1")
    assert not eva.logged_in

def test_evadb_login_correct(login_mock):
    eva = evadb_user.EvaDBUser()
    eva = eva.login("admin", "admin_pw")
    assert eva.logged_in
