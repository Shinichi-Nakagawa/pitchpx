#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import csv
# import asyncio
import yaml
import click
from bs4 import BeautifulSoup
from urllib.request import urlopen
from formencode import validators
from datetime import datetime as dt
from datetime import timedelta

from pitchpx.game.game import Game
from pitchpx.game.players import Players
from pitchpx.game.inning import Inning, AtBat, Pitch
from multiprocessing import Pool

__author__ = 'Shinichi Nakagawa'


class MlbAm(object):

    DELIMITER = '/'
    DATE_FORMAT = '%Y%m%d'
    DIRECTORY_PATH_GAME_DAY = '{year}_{month}_{day}'
    PAGE_URL_GAME_DAY = 'year_{year}/month_{month}/day_{day}'
    PAGE_URL_GAME_PREFIX = 'gid_{year}_{month}_{day}_.*'

    def __init__(self, base_dir, output, days=[], setting_file='setting.yml'):
        """
        MLBAM Data set scrape
        :param base_dir: Base directory
        :param output: Output directory
        :param days: Game Days(datetime list)
        :param setting_file: setteing file(yml)
        """
        setting = yaml.load(open(self.DELIMITER.join([base_dir, setting_file]), 'r'))
        self.url = setting['mlb']['url']
        self.parser = setting['config']['xml_parser']
        self.extension = setting['config']['extension']
        self.encoding = setting['config']['encoding']
        self.output = output
        self.days = days

    def download(self):
        """
        MLBAM dataset download
        """
        p = Pool()
        p.map(self._download, self.days)

    def _download(self, timestamp: dt):
        """
        download MLBAM Game Day
        :param timestamp: day
        """
        atbats, pitches = [], []
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
            gid_url = self.DELIMITER.join([base_url, gid_path])
            game = Game.read_xml(gid_url, self.parser, timestamp, self._get_game_number(gid_path))
            players = Players.read_xml(gid_url, self.parser)
            innings = Inning.read_xml(gid_url, self.parser, game, players)
            atbats.extend(innings.atbats)
            pitches.extend(innings.pitches)
        # writing csv
        day = "".join([timestamp_params['year'], timestamp_params['month'], timestamp_params['day']])
        self._write_csv(atbats, AtBat.DOWNLOAD_FILE_NAME.format(day=day, extension=self.extension))
        self._write_csv(pitches, Pitch.DOWNLOAD_FILE_NAME.format(day=day, extension=self.extension))

    def _get_game_number(self, gid_path):
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

    def _write_csv(self, datasets, filename):
        """
        Write CSV
        :param datasets: Datasets
        :param filename: File Name
        """
        with open('/'.join([self.output, filename]), mode='w', encoding=self.encoding) as write_file:
            writer = csv.writer(write_file, delimiter=',')
            for i, row in enumerate(datasets):
                if i == 0:
                    # header
                    writer.writerow(row.keys())
                writer.writerow(row.values())

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
    def scrape(cls, start, end, output):
        """
        Scrape a MLBAM Data
        :param start: Start Day(YYYYMMDD)
        :param end: End Day(YYYYMMDD)
        :param output: Output directory
        """

        # validate
        for param_day in ({'name': 'Start Day', 'value': start}, {'name': 'End Day', 'value': end}):
            try:
                cls._validate_datetime(param_day['value'])
            except (validators.Invalid, MlbAmException) as e:
                raise MlbAmException('{msg} a {name}.'.format(name=param_day['name'], msg=e.msg))
        cls._validate_datetime_from_to(start, end)

        mlb = MlbAm(os.path.dirname(os.path.abspath(__file__)), output, cls._days(start, end))
        mlb.download()


class MlbAmException(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg


class MlbAmBadParameter(MlbAmException):
    pass


@click.command()
@click.option('--start', '-s', required=True, help='Start Day(YYYYMMDD)')
@click.option('--end', '-e', required=True, help='End Day(YYYYMMDD)')
@click.option('--out', '-o', required=True, default='../output/mlb', help='Output directory(default:"./output/mlb")')
def scrape(start, end, out):
    """
    Scrape a MLBAM Data
    :param start: Start Day(YYYYMMDD)
    :param end: End Day(YYYYMMDD)
    :param out: Output directory(default:"../output/mlb")
    """
    try:
        MlbAm.scrape(start, end, out)
    except MlbAmBadParameter as e:
        raise click.BadParameter(e)

if __name__ == '__main__':
    scrape()
