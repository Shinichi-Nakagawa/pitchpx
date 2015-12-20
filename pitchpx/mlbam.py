#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import click
from bs4 import BeautifulSoup
from urllib.request import urlopen
from formencode import validators
from datetime import datetime as dt
from datetime import timedelta
import yaml

from pitchpx.game.game import Game
from pitchpx.game.players import Players
from pitchpx.game.inning import Inning

__author__ = 'Shinichi Nakagawa'


class MlbAm(object):

    DELIMITER = '/'
    DATE_FORMAT = '%Y%m%d'
    DIRECTORY_PATH_GAME_DAY = '{year}_{month}_{day}'
    PAGE_URL_GAME_DAY = 'year_{year}/month_{month}/day_{day}'
    PAGE_URL_GAME_PREFIX = 'gid_{year}_{month}_{day}_.*'

    def __init__(self, base_dir, setting_file='setting.yml'):
        setting = yaml.load(open(self.DELIMITER.join([base_dir, setting_file]), 'r'))
        self.output_dir = self.DELIMITER.join([base_dir, setting['mlb']['output_dir']])
        self.url = setting['mlb']['url']
        self.parser = setting['config']['xml_parser']

    def _download_game(self, ):
        pass

    def download(self, timestamp: dt):
        """
        download MLBAM Game Day
        :param timestamp:
        :return:
        """
        timestamp_params = {
            'year': str(timestamp.year),
            'month': str(timestamp.month).zfill(2),
            'day': str(timestamp.day).zfill(2)
        }
        base_url = self.DELIMITER.join([self.url, self.PAGE_URL_GAME_DAY.format(**timestamp_params)])
        html = BeautifulSoup(urlopen(base_url), self.parser)

        href = self.PAGE_URL_GAME_PREFIX.format(**timestamp_params)
        for gid in html.find_all('a', href=re.compile(href)):
            gid_path = gid.get_text().strip()
            print(gid_path)
            gid_url = self.DELIMITER.join([base_url, gid_path])
            game_number = self._get_game_number(gid_path)
            game = Game.read_xml(gid_url, self.parser, timestamp, game_number)
            players = Players.read_xml(gid_url, self.parser)
            print('get Game & Players')
            # innings = Inning.read_xml(gid_url, self.parser, game, players)
            # TODO writing csv

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
    def _days(cls, start, end):
        """
        Scrape a MLBAM Data
        :param start: Start Day(YYYYMMDD)
        :param end: End Day(YYYYMMDD)
        """
        days = []
        # datetime
        start_day, end_day = dt.strptime(start, cls.DATE_FORMAT), dt.strptime(end, cls.DATE_FORMAT)
        delta = end_day - start_day

        for day in range(delta.days+1):
            days.append(start_day + timedelta(days=day))
        return days

    @classmethod
    def _get_game_number(cls, gid_path):
        """
        Game Number
        :param gid_path: game logs directory path
        :return: game number(int)
        """
        game_number = str(gid_path[len(gid_path)-2:len(gid_path)-1])
        if game_number.isdigit():
            return int(game_number)
        else:
            raise MlbAmException('Illegal Game Number:(gid:{gid_path})'.format(gid_path))

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

        days = cls._days(start, end)

        mlb = MlbAm(os.path.dirname(os.path.abspath('.')))
        # TODO ここは並列化する
        for day in days:
            mlb.download(day)


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
