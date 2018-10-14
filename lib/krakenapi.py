import time
import urllib
import hmac
import base64
import hashlib
import requests

class HTTPSession(object):
    __instance = None
    def __new__(cls):
        if HTTPSession.__instance is None:
            s = requests.Session()
            HTTPSession.__instance = s
        return HTTPSession.__instance

def api_query_private(api_method, params, key, secret):
    urlpath = "/0/private/" + api_method
    params['nonce'] = int(1000 * time.time())
    postdata = urllib.parse.urlencode(params)
    encoded = (str(params['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    signature = hmac.new(base64.b64decode(secret),
                         message, hashlib.sha512)
    sigdigest = base64.b64encode(signature.digest())

    headers = {
        'API-Key': key,
        'API-Sign': sigdigest.decode()
    }

    r = HTTPSession().post('https://api.kraken.com' + urlpath, data=params, headers=headers, timeout=10)
    return r.json()

def api_query_public(api_method, params):
    urlbase = 'https://api.kraken.com/0/public/'
    r = HTTPSession().get(urlbase + api_method, params=params)
    return r.json()
