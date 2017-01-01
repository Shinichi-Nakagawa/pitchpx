#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from pitchpx.mlbam_util import MlbamUtil, MlbamConst


__author__ = 'Shinichi Nakagawa'


class BoxScore(object):
    """
    MLBAM Box Score Data
    """
    FILENAME = 'boxscore.xml'
    DOWNLOAD_FILE_NAME = 'mlbam_boxscore_{day}.{extension}'

    retro_game_id = MlbamConst.UNKNOWN_FULL
    home_team_id = MlbamConst.UNKNOWN_FULL
    away_team_id = MlbamConst.UNKNOWN_FULL
    home_pitchings = []
    home_battings = []
    away_pitchings = []
    away_battings = []

    def __init__(self, game, players):
        """
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        """
        self.game = game
        self.players = players

    def row(self):
        """
        Box Score Dataset(Row)
        :return: boxscore dataset(dict)
        """
        row = OrderedDict()
        row['retro_game_id'] = self.retro_game_id
        row['home_team_id'] = self.home_team_id
        row['away_team_id'] = self.away_team_id
        return row

    @classmethod
    def read_xml(cls, url, features, game, players):
        """
        read xml object
        :param url: contents url
        :param features: markup provider
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :return: pitchpx.box_score.box_score.BoxScore object
        """
        soup = MlbamUtil.find_xml("".join([url, cls.FILENAME]), features)
        return cls._generate_object(soup, game, players)

    @classmethod
    def _generate_object(cls, soup, game, players):
        """
        get box_score data
        :param soup: Beautifulsoup object
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :return: pitchpx.box_score.box_score.BoxScore object
        """
        box_score = BoxScore(game, players)
        box_score.retro_game_id = game.retro_game_id
        box_score.home_team_id = game.home_team_id
        box_score.away_team_id = game.away_team_id
        home_batting = soup.find('batting', attrs={'team_flag': 'home'})
        away_batting = soup.find('batting', attrs={'team_flag': 'away'})
        box_score.home_battings = [box_score._get_batter(b) for b in home_batting.find_all('batter')]
        box_score.away_battings = [box_score._get_batter(b) for b in away_batting.find_all('batter')]

        return box_score

    def _get_batter(self, batter):
        """
        get batter object
        :param batter: Beautifulsoup object(batter element)
        :return: batter(dict)
        """
        values = OrderedDict()
        player = self.players.rosters.get(batter.get('id'))
        bo, starting = self._get_batting_order_starting_flg(batter)
        values['bo'] = bo
        values['pos'] = batter.get('pos', MlbamConst.UNKNOWN_SHORT)
        values['id'] = batter.get('id', MlbamConst.UNKNOWN_SHORT)
        values['first'] = player.first
        values['last'] = player.last
        values['box_name'] = player.box_name
        values['rl'] = player.rl
        values['bats'] = player.bats
        values['starting'] = starting
        return values

    @classmethod
    def _get_batting_order_starting_flg(cls, batter):
        """
        get batting order and starting member flg
        :param batter: Beautifulsoup object(batter element)
        :return: batting order(1-9), starting member flg(True or False)
        """
        bo = batter.get('bo', '000')
        if bo == '000' or len(bo) != 3:
            return MlbamConst.UNKNOWN_SHORT, MlbamConst.UNKNOWN_SHORT
        batting_order = bo[:1]
        starting = True if bo[1:3] == '00' else False
        return batting_order, starting

