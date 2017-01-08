#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import csv
import yaml
import click
import logging
from multiprocessing import Pool
from formencode import validators
from datetime import datetime as dt
from datetime import timedelta
import time

from pitchpx.mlbam_util import MlbamUtil, MlbAmException, MlbAmHttpNotFound, MlbAmBadParameter
from pitchpx.game.game import Game
from pitchpx.game.players import Players
from pitchpx.game.boxscore import BoxScore
from pitchpx.game.inning import Inning, AtBat, Pitch, InningAction

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

    def _download(self, timestamp):
        """
        download MLBAM Game Day
        :param timestamp: day
        """
        games, atbats, pitches = [], [], []
        rosters, coaches, umpires = [], [], []
        boxscores, actions = [], []
        timestamp_params = {
            'year': str(timestamp.year),
            'month': str(timestamp.month).zfill(2),
            'day': str(timestamp.day).zfill(2)
        }

        logging.info('->- Game data download start({year}/{month}/{day})'.format(**timestamp_params))

        base_url = self.DELIMITER.join([self.url, self.PAGE_URL_GAME_DAY.format(**timestamp_params)])
        html = MlbamUtil.find_xml(base_url, self.parser)

        href = self.PAGE_URL_GAME_PREFIX.format(**timestamp_params)
        for gid in html.find_all('a', href=re.compile(href)):
            gid_path = gid.get_text().strip()
            gid_url = self.DELIMITER.join([base_url, gid_path])
            # Read XML & create dataset
            try:
                game = Game.read_xml(gid_url, self.parser, timestamp, MlbAm._get_game_number(gid_path))
                players = Players.read_xml(gid_url, self.parser, game)
                innings = Inning.read_xml(gid_url, self.parser, game, players)
                boxscore = BoxScore.read_xml(gid_url, self.parser, game, players)
            except MlbAmHttpNotFound as e:
                logging.warning(e.msg)
                continue

            # append a dataset
            games.append(game.row())
            rosters.extend([roseter.row() for roseter in players.rosters.values()])
            coaches.extend([coach.row() for coach in players.coaches.values()])
            umpires.extend([umpire.row() for umpire in players.umpires.values()])
            atbats.extend(innings.atbats)
            pitches.extend(innings.pitches)
            actions.extend(innings.actions)
            boxscores.append(boxscore.row())

        # writing csv
        day = "".join([timestamp_params['year'], timestamp_params['month'], timestamp_params['day']])
        for params in (
                {'datasets': games, 'filename': Game.DOWNLOAD_FILE_NAME},
                {'datasets': rosters, 'filename': Players.Player.DOWNLOAD_FILE_NAME},
                {'datasets': coaches, 'filename': Players.Coach.DOWNLOAD_FILE_NAME},
                {'datasets': umpires, 'filename': Players.Umpire.DOWNLOAD_FILE_NAME},
                {'datasets': atbats, 'filename': AtBat.DOWNLOAD_FILE_NAME},
                {'datasets': pitches, 'filename': Pitch.DOWNLOAD_FILE_NAME},
                {'datasets': boxscores, 'filename': BoxScore.DOWNLOAD_FILE_NAME},
                {'datasets': actions, 'filename': InningAction.DOWNLOAD_FILE_NAME},
        ):
            self._write_csv(params['datasets'], params['filename'].format(day=day, extension=self.extension))
        time.sleep(2)

        logging.info('-<- Game data download end({year}/{month}/{day})'.format(**timestamp_params))

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
            for char in reversed(gid_path):
                if char.isdigit():
                    return int(char)
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
                    writer.writerow(list(row.keys()))
                writer.writerow(list(row.values()))

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
        # Logger setting
        logging.basicConfig(
            level=logging.INFO,
            format="time:%(asctime)s.%(msecs)03d" + "\tmessage:%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # validate
        for param_day in ({'name': 'Start Day', 'value': start}, {'name': 'End Day', 'value': end}):
            try:
                cls._validate_datetime(param_day['value'])
            except (validators.Invalid, MlbAmException) as e:
                raise MlbAmException('{msg} a {name}.'.format(name=param_day['name'], msg=e.msg))
        cls._validate_datetime_from_to(start, end)

        # Download
        logging.info('->- MLBAM dataset download start')
        mlb = MlbAm(os.path.dirname(os.path.abspath(__file__)), output, cls._days(start, end))
        mlb.download()
        logging.info('-<- MLBAM dataset download end')


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
        logging.basicConfig(level=logging.DEBUG)
        MlbAm.scrape(start, end, out)
    except MlbAmBadParameter as e:
        raise click.BadParameter(e)

if __name__ == '__main__':
    scrape()
