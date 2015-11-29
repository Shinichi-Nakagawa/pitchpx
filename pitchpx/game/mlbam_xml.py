#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

__author__ = 'Shinichi Nakagawa'


class MlbamXml(object):

    @classmethod
    def find_xml(cls, url, markup, tag, href):
        """
        find xml
        :param url: contents url
        :param markup: markup provider
        :param tag: find tag
        :param href: xml file path
        :return: BeautifulSoup object
        """
        return BeautifulSoup(urlopen(url), markup).find(tag, href=href)

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
