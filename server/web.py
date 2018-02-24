#!/usr/bin/env python3

import re
import http.client
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl, urlencode

class JoliSoup(BeautifulSoup):
    def __new__(cls, txt):
        soup = super().__new__(cls)
        if isinstance(txt, bytes):
            txt = txt.decode()
        soup.__init__(txt, 'lxml')
        ltxt = txt.lower()
        obj = soup.html.body.find_all(recursive=False)[0]
        def get_old_case(s, before='', after=''):
            match = re.compile('{}{}{}'.format(before, s, after)).search(ltxt)
            if match is None:
                raise RuntimeError('"{}" not found in soup'.format(s))
            begin, end = match.span()
            zone = txt[begin:end]
            idx = zone.lower().index(s)
            if idx < 0:
                raise RuntimeError('"{}" not found in soup'.format(s))
            return zone[idx:len(before)+len(s)]

        old_tags = {}
        def get_tag_case(s):
            if not s in old_tags:
                old_tags[s] = get_old_case(s, before='< *')
            return old_tags[s]

        old_attrs = {}
        def get_attr_case(s):
            if not s in old_attrs:
                old_attrs[s] = get_old_case(s, after=' *=')
            return old_attrs[s]

        def change(item):
            item.name = get_tag_case(item.name)
            attrs = dict(item.attrs)
            for attr, value in attrs.items():
                del item.attrs[attr]
                item.attrs[get_attr_case(attr)] = value
            for child in item.find_all(recursive=False):
                change(child)
        change(obj)
        return obj

class UrlArgs:
    @staticmethod
    def args2dict(s):
        return { key: value for key, value in parse_qsl(s) }
    @staticmethod
    def dict2args(d):
        return urlencode(list(d.items()))

class Cooker(http.client.HTTPSConnection):
    def __init__(self, *ag, **kw):
        super().__init__(*ag, **kw)
        self.cookies = {}
    def request(self, method, url, body=None, headers={}, decode=lambda i:i):
        headers = { k:v for k,v in headers.items() }
        handle_cookie = not 'Cookie' in headers
        if handle_cookie:
            headers['Cookie'] = '; '.join((
                '{}={}'.format(key, value)
                for key, value in self.cookies.items()
            ))
        if isinstance(body, dict):
            body = UrlArgs.dict2args(body)
        super().request(method, url, body, headers)
        resp = self.getresponse()
        resp.data = decode(resp.read())
        new_cookies = resp.getheader('Set-Cookie')
        if new_cookies and handle_cookie:
            for cookie in new_cookies.split(','):
                key, value = cookie.split(';')[0].strip().split('=')
                self.cookies[key] = value
        return resp
