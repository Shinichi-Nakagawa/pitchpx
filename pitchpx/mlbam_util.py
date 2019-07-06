#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import requests

__author__ = 'Shinichi Nakagawa'


class MlbamUtil(object):

    HTTP_HEADERS = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    @classmethod
    def _get_content(cls, url, headers=HTTP_HEADERS):
        """
        Get http content
        :param url: contents url
        :param headers: http header
        :return: BeautifulSoup object
        """
        session = requests.Session()
        return session.get(url, headers=headers)

    @classmethod
    def find_xml(cls, url, features):
        """
        find xml
        :param url: contents url
        :param features: markup provider
        :param headers: http header
        :return: BeautifulSoup object
        """
        req = cls._get_content(url)
        if req.status_code in range(200, 300):
            return BeautifulSoup(req.text, features)
        else:
            raise MlbAmHttpNotFound('HTTP Error url: {url} status: {status}'.format(url=url, status=req.status_code))

    @classmethod
    def find_xml_all(cls, url, markup, tag, pattern):
        """
        find xml(list)
        :param url: contents url
        :param markup: markup provider
        :param tag: find tag
        :param pattern: xml file pattern
        :return: BeautifulSoup object list
        """
        body = cls.find_xml(url, markup)
        return body.find_all(tag, href=re.compile(pattern))

    @classmethod
    def get_attribute(cls, soup, key, unknown=None):
        """
        Get attribute for Beautifulsoup object
        :param soup: Beautifulsoup object
        :param key: attribute key
        :param unknown: attribute key not exists value(default:None)
        :return: attribute value
        """
        if key in soup.attrs:
            return soup.get(key)
        return unknown

    @classmethod
    def get_attribute_stats(cls, soup, key, data_type=str, unknown=None):
        """
        Get attribute for Beautifulsoup object
        :param soup: Beautifulsoup object
        :param key: attribute key
        :param data_type: Data type(int, float, etc...)
        :param unknown: attribute key not exists value(default:None)
        :return: (data_type)attribute value
        """
        value = cls.get_attribute(soup, key, unknown=unknown)

        if value in ('placeholder', 'None'):
            return unknown
        elif value and value != unknown:
            return data_type(value)
        return unknown


class MlbamConst(object):

    UNKNOWN_FULL = 'Unknown'
    UNKNOWN_SHORT = 'U'
    FLG_TRUE = 'T'
    FLG_FALSE = 'F'


class MlbAmException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg


class MlbAmBadParameter(MlbAmException):
    pass


class MlbAmHttpNotFound(MlbAmException):
    pass
