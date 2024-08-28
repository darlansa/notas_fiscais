from datetime import datetime

import requests
from parsel import Selector


def converte_data(data):
    print(type(data))
    return datetime.strptime(data, "%Y-%m-%d").date()


def valida_url(url):
    try:
        r = requests.get(url=url)
        if r.status_code == 200:
            return r, True, "OK"
    except requests.exceptions.MissingSchema:
        return 0, False, "MissingSchema"
    except requests.exceptions.ConnectionError:
        return 0, False, "ConnectionError"
    except requests.exceptions.ProxyError:
        return 0, False, "ProxyError"
    except requests.exceptions.SSLError:
        return 0, False, "SSLError"
    except requests.exceptions.Timeout:
        return 0, False, "Timeout"
    except requests.exceptions.ConnectTimeout:
        return 0, False, "ConnectTimeout"
    except requests.exceptions.InvalidURL:
        return 0, False, "InvalidURL"
    except requests.exceptions.InvalidSchema:
        return 0, False, "InvalidSchema"
