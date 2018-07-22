import re
import urllib.parse

EMAIL_RE = re.compile(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)',
                      re.UNICODE)
URL_RE = re.compile(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',
                    re.UNICODE)


def get_nth(x, y=None, n=0):
    if x:
        try:
            return x[n]
        except IndexError:
            return y
    return y


def clean_link(url, param='q'):
    if not url.startswith('/redirect'):
        return url
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)[param][0]


def extract_links(text):
    return URL_RE.findall(text)


def extract_emails(text):
    return EMAIL_RE.findall(text)
