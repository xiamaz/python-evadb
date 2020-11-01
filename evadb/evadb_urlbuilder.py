EVADB_SHARED_PAGES = {
}

EVADB_USER_PAGES = {
    "login_page": "/login.pl",
    "login_call": "/loginDo.pl",
    "search_ad_page": "/search.pl",
    "search_ad_call": "/searchDo.pl",
    "search_ar_page": "/searchGeneInd.pl",
    "search_ar_call": "/searchGeneIndDo.pl",
    "search_sample_page": "/searchStat.pl",
    "search_sample_call": "/searchSampleDo.pl",
}

EVADB_ADMIN_PAGES = {
}


def build_evadb_urls(host, user_loc="", admin_loc=""):
    """Generate correct evadb page urls based on whether both user and admin
    components follow the canonical folder structure or the revised structure
    in the dockerized version.
    """
    urls = {
        **{k: host + v for k, v in EVADB_SHARED_PAGES.items()},
        **{k: host + user_loc + v for k, v in EVADB_USER_PAGES.items()},
        **{k: host + admin_loc + v for k, v in EVADB_ADMIN_PAGES.items()},
    }
    return urls
