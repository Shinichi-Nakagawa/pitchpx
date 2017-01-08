#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

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
    home_pitching = []
    home_batting = []
    away_pitching = []
    away_batting = []

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
        :return: {
            'retro_game_id': Retrosheet Game id
            'home_team_id': Home Team Id
            'away_team_id': Away Team Id
            'home_lineup_[1-9]_id': Starting Member Player Id(Home)
            'home_lineup_[1-9]_name': Starting Member Player Box Name(Home)
            'home_lineup_[1-9]_pos': Starting Member Player Position(Home)
            'home_batter': Home Batters(JSON)
            'home_batter': Home Pitchers(JSON)
            'away_lineup_[1-9]_id': Starting Member Player Id(Away)
            'away_lineup_[1-9]_name': Starting Member Player Box Name(Away)
            'away_lineup_[1-9]_pos': Starting Member Player Position(Away)
            'away_batter': Away Batters(JSON)
            'away_batter': Away Pitchers(JSON)
        }
        """
        row = OrderedDict()
        row['retro_game_id'] = self.retro_game_id
        row['home_team_id'] = self.home_team_id
        row['away_team_id'] = self.away_team_id
        for b in self.home_batting:
            if not b['starting']:
                continue
            row['home_lineup_{bo}_id'.format(**b)] = b.get('id')
            row['home_lineup_{bo}_name'.format(**b)] = b.get('box_name')
            row['home_lineup_{bo}_pos'.format(**b)] = b.get('pos')
        row['home_batter'] = json.dumps(self.home_batting)
        row['home_pitcher'] = json.dumps(self.home_pitching)
        for b in self.away_batting:
            if not b['starting']:
                continue
            row['away_lineup_{bo}_id'.format(**b)] = b.get('id')
            row['away_lineup_{bo}_name'.format(**b)] = b.get('box_name')
            row['away_lineup_{bo}_pos'.format(**b)] = b.get('pos')
        row['away_batter'] = json.dumps(self.away_batting)
        row['away_pitcher'] = json.dumps(self.away_pitching)
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

        def get_batter(soup, team_flag):
            batting = soup.find('batting', attrs={'team_flag': team_flag})
            if batting:
                return batting.find_all('batter')
            return []

        def get_pitcher(soup, team_flag):
            pitching = soup.find('pitching', attrs={'team_flag': team_flag})
            if pitching:
                return pitching.find_all('pitcher')
            return []

        box_score = BoxScore(game, players)

        box_score.retro_game_id = game.retro_game_id
        box_score.home_team_id = game.home_team_id
        box_score.away_team_id = game.away_team_id
        box_score.home_batting = [box_score._get_batter(b) for b in get_batter(soup, 'home')]
        box_score.away_batting = [box_score._get_batter(b) for b in get_batter(soup, 'away')]
        box_score.home_pitching = [box_score._get_pitcher(p) for p in get_pitcher(soup, 'home')]
        box_score.away_pitching = [box_score._get_pitcher(p) for p in get_pitcher(soup, 'away')]

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
        bo = batter.get('bo', None)
        if not bo or len(bo) != 3:
            return False, False
        batting_order = bo[:1]
        starting = True if bo[1:3] == '00' else False
        return batting_order, starting

    def _get_pitcher(self, pitcher):
        """
        get pitcher object
        :param pitcher: Beautifulsoup object(pitcher element)
        :return: pitcher(dict)
        """
        values = OrderedDict()
        player = self.players.rosters.get(pitcher.get('id'))
        values['pos'] = pitcher.get('pos', MlbamConst.UNKNOWN_SHORT)
        values['id'] = pitcher.get('id', MlbamConst.UNKNOWN_SHORT)
        values['first'] = player.first
        values['last'] = player.last
        values['box_name'] = player.box_name
        values['rl'] = player.rl
        values['bats'] = player.bats
        values['out'] = pitcher.get('out', MlbamConst.UNKNOWN_SHORT)
        values['bf'] = pitcher.get('bf', MlbamConst.UNKNOWN_SHORT)
        return values

