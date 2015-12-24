#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
from pitchpx.mlbam_util import MlbamUtil, MlbamConst
from pitchpx.game.game import Game
from pitchpx.game.players import Players

__author__ = 'Shinichi Nakagawa'


class Pitch(object):

    @classmethod
    def row(cls, ab, game: Game, players: Players, inning_number: int, inning_id: int) -> dict:
        """
        Pitching Result
        :param ab: at bat object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :param inning_number: Inning Number
        :param inning_number: Inning Id(0:home 1:away)
        :return: row value(dict)
        """
        return {
            # TODO pitching stats
        }

class AtBat(object):

    @classmethod
    def row(cls, ab, game: Game, players: Players, inning_number: int, inning_id: int, pitch_list: list) -> dict:
        """
        At Bat Result
        :param ab: at bat object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home 1:away)
        :param pitch_list: Pitching
        :return: row value(dict)
        """
        return {
            'retro_game_id': game.retro_game_id,
            'year': game.timestamp.year,
            'month': game.timestamp.month,
            'day': game.timestamp.day,
            'st_fl': game.st_fl,
            'regseason_fl': game.regseason_fl,
            'playoff_fl': game.playoff_fl,
            'game_type': game.game_type,
            'game_type_des': game.game_type_des,
            'local_game_time': game.local_game_time,
            'game_id': game.game_id,
            'home_team_id': game.home_team_id,
            'away_team_id': game.away_team_id,
            'home_team_lg': game.home_team_lg,
            'away_team_lg': game.away_team_lg,
            'interleague_fl': game.interleague_fl,
            'park_id': game.park_id,
            'park_name': game.park_name,
            'park_location': game.park_loc,
            'inning_number': inning_number,
            'bat_home_id': inning_id,
            'inn_outs': MlbamUtil.get_attribute_stats(ab, 'o', int, None),
            'ab_number': MlbamUtil.get_attribute_stats(ab, 'num', int, None),
            'pit_mlbid': MlbamUtil.get_attribute_stats(ab, 'pitcher', str, MlbamConst.UNKNOWN_FULL),
            'pit_hand_cd': MlbamUtil.get_attribute_stats(ab, 'p_throws', str, MlbamConst.UNKNOWN_FULL),
            'bat_mlbid': MlbamUtil.get_attribute_stats(ab, 'batter', str, MlbamConst.UNKNOWN_FULL),
            'bat_hand_cd': MlbamUtil.get_attribute_stats(ab, 'stand', str, MlbamConst.UNKNOWN_FULL),
            'ball_ct': MlbamUtil.get_attribute_stats(ab, 'b', int, None),
            'strike_ct': MlbamUtil.get_attribute_stats(ab, 's', int, None),
            'pitch_seq': None,  # TODO pitchタグを数えて出す
            'pitch_type_seq': None,  # TODO pitchタグを数えて出す
            'event_outs_ct': None,  # TODO 数える
            'ab_des': MlbamUtil.get_attribute_stats(ab, 'des', str, MlbamConst.UNKNOWN_FULL),
            'event_tx': MlbamUtil.get_attribute_stats(ab, 'event', str, MlbamConst.UNKNOWN_FULL),
            'event_cd': MlbamUtil.get_attribute_stats(ab, 'event_num', int, None),
            'battedball_cd': None,  # TODO event_cdから出す,
            'start_bases_cd': None,  # TODO 塁上のランナー数(開始時)
            'end_bases_cd': None,  # TODO 塁上のランナー数(終了時)
        }


class Inning(object):

    DIRECTORY = 'inning'
    FILENAME_PATTERN = 'inning_\d*.xml'
    TAG = 'a'
    INNING_TOP = 'top'
    INNING_BOTTOM = 'bottom'
    INNINGS = {
        INNING_TOP: 0,
        INNING_BOTTOM: 1,
    }
    atbats = []
    pitches = []

    def __init__(self, game, players):
        """
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        """
        self.game = game
        self.players = players

    @classmethod
    def read_xml(cls, url, markup, game, players):
        """
        read xml object
        :param url: contents url
        :param markup: markup provider
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :return: pitchpx.game.game.Game object
        """
        innings = Inning(game, players)
        base_url = "".join([url, cls.DIRECTORY])
        for inning in MlbamUtil.find_xml_all(base_url, markup, cls.TAG, cls.FILENAME_PATTERN):
            soup = MlbamUtil.find_xml("/".join([base_url, inning.get_text().strip()]), markup)
            inning_number = int(soup.inning['num'])
            for inning in cls.INNINGS.keys():
                inning_soup = soup.inning.find(inning)
                innings._inning_events(inning_soup, inning_number, cls.INNINGS[inning])
        return innings

    def _inning_events(self, soup, inning_number, inning_id):
        """
        Inning Events.
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        """
        # at bat(batter box data) & pitching data
        for ab in soup.find_all('atbat'):
            pitching_stats = self._get_pitch(ab, inning_number, inning_id)
            self.atbats.append(self._get_atbat(ab, inning_number, inning_id, pitching_stats))

    def _get_atbat(self, soup, inning_number, inning_id, pitching):
        """
        get atbat data
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        :param pitching: pitching event list
        :return: atbat result
        """
        return AtBat.row(soup, self.game, self.players, inning_number, inning_id, pitching)

    def _get_pitch(self, soup, inning_number, inning_id):
        """
        get pitch data
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        :return: pitches result(list)
        """
        pitches = []
        for pitch in soup.find_all('pitch'):
            # TODO append pitch event
            pitches.append(Pitch.row(pitch, self.game, self.players, inning_number, inning_id))
        return pitches
