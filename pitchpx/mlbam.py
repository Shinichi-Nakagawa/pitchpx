#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
from bs4 import BeautifulSoup
from urllib.request import urlopen
from formencode import validators
import yaml

__author__ = 'Shinichi Nakagawa'


class MlbAm(object):

    def __init__(self, base_dir, setting_file='setting.yml'):
        self.setting = yaml.load(open('/'.join([base_dir, setting_file]), 'r'))
        self.output_dir = '/'.join([base_dir, self.setting['mlb']['output_dir']])
        self.html = BeautifulSoup(urlopen(self.setting['mlb']['url']), self.setting['config']['xml_parser'])

    def get(self, ):
        pass

    @classmethod
    def _validate_datetime(cls, value):
        """
        validate datetime value
        :param value: datetime value
        :return: None or validators.Invalid or MlbAmException
        """
        datetime_check = validators.Int()
        datetime_check.to_python(value)
        if len(value) != 8:
            raise MlbAmException("Length Error:{value}({length})".format(value=value, length=len(value)))

    @classmethod
    def _validate_datetime_from_to(cls, start, end):
        """
        validate from-to
        :param start: Start Day(YYYYMMDD)
        :param end: End Day(YYYYMMDD)
        :return: None or MlbAmException
        """
        if not start <= end:
            raise MlbAmException("not Start Day({start}) <= End Day({end})".format(start=start, end=end))

    @classmethod
    def scrape(cls, start, end):
        """
        Scrape a MLBAM Data
        :param start: Start Day(YYYYMMDD)
        :param end: End Day(YYYYMMDD)
        """

        for param_day in ({'name': 'Start Day', 'value': start}, {'name': 'End Day', 'value': end}):
            try:
                cls._validate_datetime(param_day['value'])
            except (validators.Invalid, MlbAmException) as e:
                raise click.BadParameter('{msg} a {name}.'.format(name=param_day['name'], msg=e.msg))

        mlb = MlbAm(os.path.dirname(os.path.abspath('.')))
        mlb.get()


class MlbAmException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg


@click.command()
@click.option('--start', '-s', required=True, help='Start Day(YYYYMMDD)')
@click.option('--end', '-e', required=True, help='End Day(YYYYMMDD)')
def scrape(start, end):
    """
    Scrape a MLBAM Data
    :param start: Start Day(YYYYMMDD)
    :param end: End Day(YYYYMMDD)
    """
    try:
        MlbAm.scrape(start, end)
    except MlbAmException as e:
        raise click.BadParameter('{msg} a {name}.'.format(name=param_day['name'], msg=e.msg))

if __name__ == '__main__':
    scrape()
