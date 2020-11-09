EVADB_USER_PAGES = {
    "login_page": "/login.pl",
    "login_call": "/loginDo.pl",
    "search_ad_page": "/search.pl",
    "search_ad_call": "/searchDo.pl",
    "search_ar_page": "/searchGeneInd.pl",
    "search_ar_call": "/searchGeneIndDo.pl",
    "search_sample_page": "/searchStat.pl",
    "search_sample_call": "/searchSampleDo.pl",
    "show_hpo_page": "/showHPO.pl",
}

EVADB_ADMIN_PAGES = {
}


def build_evadb_urls(user_host, admin_host):
    urls = {
        **{k: user_host + v for k, v in EVADB_USER_PAGES.items()},
        **{k: admin_host + v for k, v in EVADB_ADMIN_PAGES.items()},
    }
    return urls
