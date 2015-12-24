#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

__author__ = 'Shinichi Nakagawa'


class MlbamUtil(object):

    @classmethod
    def find_xml(cls, url, markup):
        """
        find xml
        :param url: contents url
        :param markup: markup provider
        :return: BeautifulSoup object
        """
        return BeautifulSoup(urlopen(url), markup)

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
        return BeautifulSoup(urlopen(url), markup).find_all(tag, href=re.compile(pattern))

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


class MlbamConst(object):

    UNKNOWN_FULL = 'Unknown'
    UNKNOWN_SHORT = 'U'
    FLG_TRUE = 'T'
    FLG_FALSE = 'F'
