import os
import re
import requests
from html.parser import HTMLParser
from html.entities import name2codepoint
from pynautobot.core.api import Api
from pynautobot.core.query import Request
from pynautobot.models.dcim import Devices
import pynautobot


def auth_nautobot_api() -> Api:
    url = os.environ.get('NAUTOBOT_URL', 'http://localhost:8080')
    token = fetch_create_nautobot_api_token(url)
    api = pynautobot.api(
        url=url,
        token=token,
        threading=True
    )
    return api


def fetch_create_nautobot_api_token(url: str) -> str:
    username = os.environ.get('NAUTOBOT_USER', 'admin')
    password = os.environ.get('NAUTOBOT_PASSWORD', 'admin')
    headers = {
        "Accept": "application/json; indent=4",
    }
    sesh = requests.sessions.Session()
    sesh.auth = (username, password)
    res: requests.Response = sesh.post(
        url + "/api/users/tokens/", headers=headers)
    return res.json().get("key")


def fetch_nautobot_generic(nautobot: Api, url: str, filters: dict[str] | None = None):
    '''
    fetch any url endpoint from nautobot
    returns a list of results from the endpoint poll
    '''
    req = Request(
        base=url,
        token=nautobot.token,
        http_session=nautobot.http_session,
        api_version=nautobot.api_version,
        filters=filters
    )
    res = req.get()
    return res


def fetch_nautobot_devices(nautobot: Api, match_names: list[str]) -> list[Devices]:
    '''
    Poll Nautobot for its devices and compare to a list of devices from OneView
    '''
    nautobot_virutal_connect_devices: Devices = nautobot.dcim.devices.filter(
        name__ic=match_names)
    return nautobot_virutal_connect_devices


def fetch_nautobot_sessionid(nautobot: Api, csrf_middleware_token: str) -> str:
    '''
    For endpoints that do not support API calls, fetch a sessionid to pass nautobot's checks
    You may have to provide this sessionid string as a cookie or HTML form value
    '''
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        # "Authorization": f"Token {nautobot.token}",
    }
    body: dict = {
        "csrfmiddlewaretoken": csrf_middleware_token,
        "next": "/",
        "username": os.environ.get('NAUTOBOT_USER', 'admin'),
        "password": os.environ.get('NAUTOBOT_PASSWORD', 'admin')
    }

    res: requests.Response = requests.post(nautobot.base_url.replace(
        "/api", "") + "/login/", data=body, headers=headers, cookies=nautobot.http_session.cookies, allow_redirects=False)
    res_headers: str = res.raw.headers.get('Set-Cookie')
    session_id = re.search("(?<=sessionid=)(.*?)(?=;)", res_headers)
    if session_id:
        return session_id.group(0)
    return None


def fetch_nautobot_form_content(nautobot: Api, url: str, content_name: str) -> tuple[str]:
    '''
    For endpoints that require a form submission instead of API call,
    fetch the middleware CSRF token.
    You may have to provide this as a form field or cookie
    '''
    class CsrfMiddlewareHTMLParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.messages: set = set([])

        def handle_starttag(self, tag, attrs):
            # print("Start tag:", tag)
            is_my_key: bool = False
            for attr in attrs:
                # print("     attr scan:", attr)
                if attr == ('name', content_name):
                    is_my_key = True
            if is_my_key:
                for attr in attrs:
                    if attr[0] == 'value':
                        # print("found a value", content_name, "in HTML!")
                        # print(attr)
                        self.messages.add(attr[1])
    parser: HTMLParser = CsrfMiddlewareHTMLParser()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;",
        "Authorization": f"Token {nautobot.token}",
    }
    res = requests.get(
        url, cookies=nautobot.http_session.cookies, headers=headers)
    csrf_token = res.cookies.get('csrftoken')
    parser.feed(res.text)
    if len(parser.messages) != 0:
        csrf_middleware_token: str = list(parser.messages)[0]
    else:
        print("WARN: was not able to find requested HTTP form content from Nautobot: ", content_name)
        csrf_middleware_token = None
    return csrf_token, csrf_middleware_token
