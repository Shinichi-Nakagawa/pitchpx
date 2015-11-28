#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
from bs4 import BeautifulSoup
from urllib.request import urlopen
from formencode import validators
from datetime import datetime as dt
from datetime import timedelta
import yaml

__author__ = 'Shinichi Nakagawa'


class MlbAm(object):

    DATE_FORMAT = '%Y%m%d'

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
            raise MlbAmBadParameter("Length Error:{value}({length})".format(value=value, length=len(value)))

    @classmethod
    def _validate_datetime_from_to(cls, start, end):
        """
        validate from-to
        :param start: Start Day(YYYYMMDD)
        :param end: End Day(YYYYMMDD)
        :return: None or MlbAmException
        """
        if not start <= end:
            raise MlbAmBadParameter("not Start Day({start}) <= End Day({end})".format(start=start, end=end))

    @classmethod
    def scrape(cls, start, end):
        """
        Scrape a MLBAM Data
        :param start: Start Day(YYYYMMDD)
        :param end: End Day(YYYYMMDD)
        """

        # validate
        for param_day in ({'name': 'Start Day', 'value': start}, {'name': 'End Day', 'value': end}):
            try:
                cls._validate_datetime(param_day['value'])
            except (validators.Invalid, MlbAmException) as e:
                raise MlbAmException('{msg} a {name}.'.format(name=param_day['name'], msg=e.msg))
        cls._validate_datetime_from_to(start, end)

        # datetime
        start_day, end_day = dt.strptime(start, cls.DATE_FORMAT), dt.strptime(end, cls.DATE_FORMAT)
        delta = end_day - start_day

        # TODO 並列化に備えてここで日付リストをとっておく
        days = []
        for day in range(delta.days+1):
            days.append(start_day + timedelta(days=day))

        mlb = MlbAm(os.path.dirname(os.path.abspath('.')))
        mlb.get()


class MlbAmException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg


class MlbAmBadParameter(MlbAmException):
    pass


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
    except MlbAmBadParameter as e:
        raise click.BadParameter(e)

if __name__ == '__main__':
    scrape()
