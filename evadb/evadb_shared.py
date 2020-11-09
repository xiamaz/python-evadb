from collections import namedtuple
from dataclasses import dataclass

from loguru import logger
import requests

from .csrf_parser import extract_csrf_tokens


class UnauthorizedException(Exception):
    pass


Response = namedtuple("Response", ["error", "data"])


def require_login(fn):
    """Enforce that a given function will only execute if properly logged in.

    Otherwise raise an unauthorized error.
    """
    def wrapped(self, *args, **kwargs):
        if not self.logged_in:
            logger.error(f"{self.__class__.__name__}.{fn.__name__} requires authentication")
            raise UnauthorizedException()
        return fn(self, *args, **kwargs)
    return wrapped


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


def build_evadb_urls(host: str, pages: dict) -> dict:
    """Build a dict of complete URLs with the given host.
    """
    urls = {k: host + v for k, v in pages.items()}
    return urls


class EvaDBBase:

    pages = {
        "login_page": "/login.pl",
        "login_call": "/loginDo.pl",
    }

    def __init__(
        self,
        host: str,
    ):
        """
        Args:
            url: URL to the EvaDB User instance.
        """
        self._session = requests.Session()
        self.logged_in = False

        # potentially merge with pages already existing in parent class
        self._urls = build_evadb_urls(host, self.pages)

        self._session.headers["referer"] = self._urls["login_page"]

    def _obtain_csrf_token(self):
        csrf_url = self._urls["login_page"]
        resp = self._session.get(csrf_url)
        csrf_tokens = extract_csrf_tokens(resp.text)
        return csrf_tokens

    def _post_form(self, url, data):
        resp = self._session.post(url, data=data)
        resp.raise_for_status()
        return resp.text

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
