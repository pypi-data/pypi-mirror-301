import requests
import pygnparser
import os
from .result import Result

class NoResultException(Exception):
    pass


def gnp_url():
    return os.getenv("GNPARSER_BASE_URL", "https://parser.globalnames.org/")


def gnp_get(url, args, **kwargs):
    resp = requests.get(url, params=args, headers=get_agent(), **kwargs)
    resp.raise_for_status()
    
    return resp.json()
    

def gnp_post(url, args, **kwargs):
    resp = requests.post(url, data=args, headers=get_agent(), **kwargs)
    resp.raise_for_status()
    
    results = []
    for result in resp.json():
        results.append(Result(result))
    if len(results) == 1:
        results = results[0]
    return results


def gnp_query(url, args, **kwargs):

    # check if gnparser is installed locally
    if check_for_gnparser_local_install():
        pass
    else:
        return gnp_post(url, args, **kwargs)


# TODO: use local installation if available
def check_for_gnparser_local_install():
    current_version = gnp_get("https://parser.globalnames.org/api/v1/version")
    installed = True
    try:
        installed_version_array = os.popen("gnparser -V").read().strip().split("\n\n")
        installed_version = installed_version_array[0].replace("version:", "").strip()
        build_version = installed_version_array[1].replace("build:", "").strip()
        installed_version = {"version": installed_version, "build": build_version}
    except Exception:
        installed = False
    if installed_version != current_version:
        print("WARNING: installed version of gnparser is not the same as the current version")
    return installed


def get_agent():
    return {
        "user-agent": "python-requests/"
        + requests.__version__
        + ",pygnparser/"
        + pygnparser.__version__
    }

