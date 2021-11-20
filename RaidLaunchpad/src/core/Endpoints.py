import json
import requests
from .Cloudflare import *
from src.core.Util import *
from base64 import b64encode
from src.core.Container import tokens


def get_tor_session():
    tor_port = get_config("tor_port")
    tor = requests.session()
    tor.proxies = {'http': f'socks5://127.0.0.1:{tor_port}', 'https': f'socks5://127.0.0.1:{tor_port}'}
    return tor


if get_config('use_tor'):
    session = get_tor_session()
    console_log(f'Tor is connected: {session.proxies["https"]}.', 2)
else:
    session = requests.Session()

cookie_string = get_cookie()


def send(endpoint, method, token, data=None):
    if data is None:
        data = {}

    base = "https://discord.com/api/v9/"
    user_agent = rand_user_agent()

    token_data = tokens.get_token_info(token)

    device_info = {
        "os": token_data["os"],
        "browser": token_data["browser"],
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": token_data["agent"],
        "browser_version": token_data["browser_version"],
        "os_version": token_data["os_version"],
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 36127,
        "client_event_source": None
    }

    headers = {
        "Accept": "*/*",
        "Accept-language": "en-GB",
        "Authorization": token_data["token"],
        "Content-length": "90",
        "Content-type": "application/json",
        "Cookie": cookie_string,
        "Origin": "https://discord.com",
        "Sec-fetch-dest": "empty",
        "Sec-fetch-mode": "cors",
        "Sec-fetch-site": "same-origin",
        "User-agent": token_data["agent"],
        "X-debug-options": "bugReporterEnabled",
        "X-super-properties": b64encode(json.dumps(device_info).encode('utf-8')).decode("utf-8"),
    }

    if method == 'GET':
        remove = ["Content-length", "Content-type"]
        for key in remove:
            del headers[key]

        r = session.get(base + endpoint, headers=headers)
    elif method == 'POST':
        r = session.post(base + endpoint, headers=headers,
                         json=data)
    elif method == 'PUT':
        r = session.put(base + endpoint, headers=headers,
                        json=data)
    elif method == 'PATCH':
        r = session.patch(base + endpoint, headers=headers,
                          json=data)
    elif method == 'DELETE':
        r = session.delete(base + endpoint, headers=headers,
                           json=data)

    return r
