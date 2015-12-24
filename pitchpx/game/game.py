#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pitchpx.mlbam_util import MlbamUtil, MlbamConst

__author__ = 'Shinichi Nakagawa'


class Game(object):
    """
    MLBAM Game Data
    """
    FILENAME = 'game.xml'
    TEAM_TYPE_HOME = 'home'
    TEAM_TYPE_AWAY = 'away'

    st_fl = MlbamConst.UNKNOWN_SHORT
    regseason_fl = MlbamConst.UNKNOWN_SHORT
    playoff_fl = MlbamConst.UNKNOWN_SHORT
    game_type = MlbamConst.UNKNOWN_SHORT
    game_type_des = MlbamConst.UNKNOWN_FULL
    local_game_time = MlbamConst.UNKNOWN_FULL
    game_id = MlbamConst.UNKNOWN_FULL
    home_team_id = MlbamConst.UNKNOWN_FULL
    away_team_id = MlbamConst.UNKNOWN_FULL
    home_team_lg = MlbamConst.UNKNOWN_FULL
    away_team_lg = MlbamConst.UNKNOWN_FULL
    home_team_name = MlbamConst.UNKNOWN_FULL
    away_team_name = MlbamConst.UNKNOWN_FULL
    home_team_name_full = MlbamConst.UNKNOWN_FULL
    away_team_name_full = MlbamConst.UNKNOWN_FULL
    interleague_fl = MlbamConst.UNKNOWN_SHORT
    park_id = MlbamConst.UNKNOWN_FULL
    park_name = MlbamConst.UNKNOWN_FULL
    park_loc = MlbamConst.UNKNOWN_FULL
    retro_game_id = MlbamConst.UNKNOWN_FULL
    timestamp = None

    def __init__(self, timestamp):
        """
        :param timestamp: game day
        """
        self.timestamp = timestamp

    @classmethod
    def read_xml(cls, url, markup, timestamp, game_number):
        """
        read xml object
        :param url: contents url
        :param markup: markup provider
        :param timestamp: game day
        :param game_number: game number
        :return: pitchpx.game.game.Game object
        """
        soup = MlbamUtil.find_xml("/".join([url, cls.FILENAME]), markup)
        return cls._generate_game_object(soup, timestamp, game_number)

    @classmethod
    def _generate_game_object(cls, soup, timestamp, game_number):
        """
        get game data
        :param soup: Beautifulsoup object
        :param timestamp: game day
        :param game_number: game number
        :return: pitchpx.game.game.Game object
        """
        game = Game(timestamp)

        # Base Game Data(Spring Training, Regular Season, Play Off, etc...)
        game.game_type = MlbamUtil.get_attribute(soup.game, 'type', unknown=MlbamConst.UNKNOWN_SHORT)
        game.game_type_des = cls._get_game_type_des(game.game_type)
        game.st_fl = cls._get_st_fl(game.game_type)
        game.regseason_fl = cls._get_regseason_fl(game.game_type)
        game.playoff_fl = cls._get_playoff_fl(game.game_type)
        game.local_game_time = MlbamUtil.get_attribute(soup.game, 'local_game_time', unknown=MlbamConst.UNKNOWN_FULL)
        game.game_id = MlbamUtil.get_attribute(soup.game, 'game_pk', unknown=MlbamConst.UNKNOWN_FULL)

        # Team Data
        game.home_team_id = cls._get_team_attribute(soup, cls.TEAM_TYPE_HOME, 'code')
        game.home_team_lg = cls._get_team_attribute(soup, cls.TEAM_TYPE_HOME, 'league')
        game.away_team_id = cls._get_team_attribute(soup, cls.TEAM_TYPE_AWAY, 'code')
        game.away_team_lg = cls._get_team_attribute(soup, cls.TEAM_TYPE_AWAY, 'league')
        game.home_team_name = cls._get_team_attribute(soup, cls.TEAM_TYPE_HOME, 'name')
        game.away_team_name = cls._get_team_attribute(soup, cls.TEAM_TYPE_AWAY, 'name')
        game.home_team_name_full = cls._get_team_attribute(soup, cls.TEAM_TYPE_HOME, 'name_full')
        game.away_team_name_full = cls._get_team_attribute(soup, cls.TEAM_TYPE_AWAY, 'name_full')
        game.interleague_fl = cls._get_interleague_fl(game.home_team_lg, game.away_team_lg)

        # Stadium Data
        game.park_id = cls._get_stadium_attribute(soup, 'id')
        game.park_name = cls._get_stadium_attribute(soup, 'name')
        game.park_loc = cls._get_stadium_attribute(soup, 'location')

        # Retro ID
        game.retro_game_id = cls._get_retro_id(game.home_team_id, timestamp, game_number)

        return game

    @classmethod
    def _get_game_type_des(cls, game_type):
        """
        get game type description
        :param game_type: game type
        :return: game type description
        """
        if game_type == 'S':
            return 'Spring Training'
        elif game_type == 'R':
            return 'Regular Season'
        elif game_type == 'F':
            return 'Wild-card Game'
        elif game_type == 'D':
            return 'Divisional Series'
        elif game_type == 'L':
            return 'LCS'
        elif game_type == 'W':
            return 'World Series'
        return MlbamConst.UNKNOWN_FULL

    @classmethod
    def _get_st_fl(cls, game_type):
        """
        get spring training flg
        :param game_type: game type
        :return: spring training flg(T or F)
        """
        if game_type == 'S':
            return MlbamConst.FLG_TRUE
        return MlbamConst.FLG_FALSE

    @classmethod
    def _get_regseason_fl(cls, game_type):
        """
        get regular season flg
        :param game_type: game type
        :return: regular season flg(T or F)
        """
        if game_type == 'R':
            return MlbamConst.FLG_TRUE
        return MlbamConst.FLG_FALSE

    @classmethod
    def _get_playoff_fl(cls, game_type):
        """
        get play off flg
        :param game_type: game type
        :return: play off flg(T or F)
        """
        if game_type in ('F', 'D', 'L', 'W'):
            return MlbamConst.FLG_TRUE
        return MlbamConst.FLG_FALSE

    @classmethod
    def _get_team_attribute(cls, soup, team_type, name):
        """
        get team attribute
        :param soup: Beautifulsoup object
        :param team_type: team type(home or away)
        :param name: attribute name
        :return: attribute value
        """
        if soup.find('team'):
            return soup.find("team", type=team_type)[name]
        return MlbamConst.UNKNOWN_FULL

    @classmethod
    def _get_stadium_attribute(cls, soup, name):
        """
        get stadium attribute
        :param soup: Beautifulsoup object
        :param name: attribute name
        :return: attribute value
        """
        if soup.find('stadium'):
            return soup.stadium[name]
        return MlbamConst.UNKNOWN_FULL

    @classmethod
    def _get_interleague_fl(cls, home_team_lg, away_team_lg):
        """
        get inter league flg
        :param home_team_lg: home team league
        :param away_team_lg: away team league
        :return: inter league flg(T or F or U)
        """
        if (home_team_lg == MlbamConst.UNKNOWN_SHORT) or (away_team_lg == MlbamConst.UNKNOWN_SHORT):
            return MlbamConst.UNKNOWN_SHORT
        elif home_team_lg != away_team_lg:
            return MlbamConst.FLG_TRUE
        return MlbamConst.FLG_FALSE

    @classmethod
    def _get_retro_id(cls, home_team_id, timestamp, game_number):
        """
        get retro id
        :param home_team_id: home team id
        :param timestamp: game day
        :param game_number: game number
        :return: retro id
        """
        return '{home_team_id}{year}{month}{day}{game_number}'.format(
            **{
                'home_team_id': home_team_id.upper(),
                'year': timestamp.year,
                'month': timestamp.strftime('%m'),
                'day': timestamp.strftime('%d'),
                'game_number': int(game_number)-1,
            }
        )
