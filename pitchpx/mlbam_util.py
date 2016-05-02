#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

__author__ = 'Shinichi Nakagawa'


class MlbamUtil(object):

    @classmethod
    def find_xml(cls, url, features):
        """
        find xml
        :param url: contents url
        :param features: markup provider
        :return: BeautifulSoup object
        """
        try:
            return BeautifulSoup(urlopen(url), features)
        except HTTPError as e:
            msg = 'HTTP Error url: {url} msg: {msg}'.format(url=url, msg=e.msg)
            raise MlbAmHttpNotFound(msg)


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
            return soup[key]
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
        value = cls.get_attribute(soup, key, unknown)
        if value != unknown:
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
