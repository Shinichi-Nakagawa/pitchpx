#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from pitchpx.mlbam_util import MlbamUtil, MlbamConst
from pitchpx.game.game import Game
from pitchpx.game.players import Players
from pitchpx.baseball.retrosheet import RetroSheet

__author__ = 'Shinichi Nakagawa'


class Pitch(object):

    @classmethod
    def row(
            cls,
            pitch,
            ab,
            game: Game,
            players: Players,
            inning_number: int,
            inning_id: int,
            pitch_list: list,
            out_ct: int,
    ) -> dict:
        """
        Pitching Result
        :param pitch: pitch object(type:Beautifulsoup)
        :param ab: at bat object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home 1:away)
        :param pitch_list: Pitching
        :return: row value(dict)
        """
        pitch_res = MlbamUtil.get_attribute_stats(pitch, 'type', str, MlbamConst.UNKNOWN_FULL)
        pitch_seq = [pitch['pitch_res'] for pitch in pitch_list]
        pitch_seq.extend([pitch_res])
        pitch_type = MlbamUtil.get_attribute_stats(pitch, 'pitch_type', str, None)
        pitch_type_seq = [pitch['pitch_type'] for pitch in pitch_list]
        pitch_type_seq.extend([pitch_type])
        event_outs_ct = MlbamUtil.get_attribute_stats(ab, 'o', int, 0)
        return {
            'retro_game_id': game.retro_game_id,
            'year': game.timestamp.year,
            'month': game.timestamp.month,
            'day': game.timestamp.day,
            'st_fl': game.st_fl,
            'regseason_fl': game.regseason_fl,
            'playoffs_fl': game.playoff_fl,
            'game_type': game.game_type,
            'game_type_des': game.game_type_des,
            'game_id': game.game_id,
            'home_team_id': game.home_team_id,
            'away_team_id': game.away_team_id,
            'home_team_lg': game.home_team_lg,
            'away_team_lg': game.away_team_lg,
            'interleague_fl': game.interleague_fl,
            'inning_number': inning_number,
            'bat_home_id': inning_id,
            'park_id': game.park_id,
            'park_name': game.park_name,
            'park_location': game.park_loc,
            'pit_mlbid': MlbamUtil.get_attribute_stats(ab, 'pitcher', str, MlbamConst.UNKNOWN_FULL),
            'pit_hand_cd': MlbamUtil.get_attribute_stats(ab, 'p_throws', str, MlbamConst.UNKNOWN_FULL),
            'bat_mlbid': MlbamUtil.get_attribute_stats(ab, 'batter', str, MlbamConst.UNKNOWN_FULL),
            'bat_hand_cd': MlbamUtil.get_attribute_stats(ab, 'stand', str, MlbamConst.UNKNOWN_FULL),
            'pa_ball_ct': None,  # TODO 後で
            'pa_strike_ct': None, # TODO 後で
            'outs_ct': out_ct,
            'pitch_seq': ''.join(pitch_seq),
            'pa_terminal_fl': None, # TODO 後で
            'pa_event_cd': None, # TODO 後で
            'start_bases_cd': None, # TODO 後で
            'end_bases_cd': None, # TODO 後で
            'event_outs_ct': event_outs_ct,
            'ab_number': MlbamUtil.get_attribute_stats(ab, 'num', int, None),
            'pitch_res': pitch_res,
            'pitch_des': MlbamUtil.get_attribute_stats(pitch, 'des', str, MlbamConst.UNKNOWN_FULL),
            'pitch_id': MlbamUtil.get_attribute_stats(pitch, 'id', int, None),
            'x': MlbamUtil.get_attribute_stats(pitch, 'x', float, None),
            'y': MlbamUtil.get_attribute_stats(pitch, 'y', float, None),
            'start_speed': MlbamUtil.get_attribute_stats(pitch, 'start_speed', float, None),
            'end_speed': MlbamUtil.get_attribute_stats(pitch, 'end_speed', float, None),
            'sz_top': MlbamUtil.get_attribute_stats(pitch, 'sz_top', float, None),
            'sz_bottom': MlbamUtil.get_attribute_stats(pitch, 'sz_bottom', float, None),
            'pfx_x': MlbamUtil.get_attribute_stats(pitch, 'pfx_x', float, None),
            'pfx_z': MlbamUtil.get_attribute_stats(pitch, 'pfx_z', float, None),
            'px': MlbamUtil.get_attribute_stats(pitch, 'px', float, None),
            'pz': MlbamUtil.get_attribute_stats(pitch, 'pz', float, None),
            'x0': MlbamUtil.get_attribute_stats(pitch, 'x0', float, None),
            'z0': MlbamUtil.get_attribute_stats(pitch, 'z0', float, None),
            'vx0': MlbamUtil.get_attribute_stats(pitch, 'vx0', float, None),
            'vy0': MlbamUtil.get_attribute_stats(pitch, 'vy0', float, None),
            'vz0': MlbamUtil.get_attribute_stats(pitch, 'vz0', float, None),
            'ax': MlbamUtil.get_attribute_stats(pitch, 'ax', float, None),
            'ay': MlbamUtil.get_attribute_stats(pitch, 'ay', float, None),
            'az': MlbamUtil.get_attribute_stats(pitch, 'az', float, None),
            'break_y': MlbamUtil.get_attribute_stats(pitch, 'break_y', float, None),
            'break_angle': MlbamUtil.get_attribute_stats(pitch, 'break_angle', float, None),
            'break_length': MlbamUtil.get_attribute_stats(pitch, 'break_length', float, None),
            'pitch_type': pitch_type,
            'pitch_type_seq': '|'.join(pitch_type_seq),
            'type_confidence': MlbamUtil.get_attribute_stats(pitch, 'type_confidence', float, None),
            'zone': MlbamUtil.get_attribute_stats(pitch, 'zone', float, None),
            'spin_dir': MlbamUtil.get_attribute_stats(pitch, 'spin_dir', float, None),
            'spin_rate': MlbamUtil.get_attribute_stats(pitch, 'spin_rate', float, None),
            'sv_id': MlbamUtil.get_attribute_stats(pitch, 'sv_id', str, None),
        }


class AtBat(object):

    @classmethod
    def row(
            cls,
            ab,
            game: Game,
            players: Players,
            inning_number: int,
            inning_id: int,
            pitch_list: list,
            out_ct: int,
    ) -> dict:
        """
        At Bat Result
        :param ab: at bat object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home 1:away)
        :param pitch_list: Pitching
        :param out_ct: out count
        :return: row value(dict)
        """
        event_outs_ct = MlbamUtil.get_attribute_stats(ab, 'o', int, 0)
        ab_des = MlbamUtil.get_attribute_stats(ab, 'des', str, MlbamConst.UNKNOWN_FULL)
        event_tx = MlbamUtil.get_attribute_stats(ab, 'event', str, MlbamConst.UNKNOWN_FULL)
        event_cd = RetroSheet.event_cd(event_tx, ab_des)
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
            'outs_ct': out_ct,
            'ab_number': MlbamUtil.get_attribute_stats(ab, 'num', int, None),
            'pit_mlbid': MlbamUtil.get_attribute_stats(ab, 'pitcher', str, MlbamConst.UNKNOWN_FULL),
            'pit_hand_cd': MlbamUtil.get_attribute_stats(ab, 'p_throws', str, MlbamConst.UNKNOWN_FULL),
            'bat_mlbid': MlbamUtil.get_attribute_stats(ab, 'batter', str, MlbamConst.UNKNOWN_FULL),
            'bat_hand_cd': MlbamUtil.get_attribute_stats(ab, 'stand', str, MlbamConst.UNKNOWN_FULL),
            'ball_ct': MlbamUtil.get_attribute_stats(ab, 'b', int, None),
            'strike_ct': MlbamUtil.get_attribute_stats(ab, 's', int, None),
            'pitch_seq': ''.join([pitch['pitch_res'] for pitch in pitch_list]),
            'pitch_type_seq': '|'.join([pitch['pitch_type'] for pitch in pitch_list]),
            'event_outs_ct': event_outs_ct,
            'ab_des': ab_des,
            'event_tx': event_tx,
            'event_cd': event_cd,
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
    INNINGS = OrderedDict()
    INNINGS[INNING_TOP] = 0
    INNINGS[INNING_BOTTOM] = 1
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
                if inning_soup is None:
                    break
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
        out_ct = 0
        for ab in soup.find_all('atbat'):
            pitching_stats = self._get_pitch(ab, inning_number, inning_id, out_ct)
            atbat = self._get_atbat(ab, inning_number, inning_id, pitching_stats, out_ct)
            self.atbats.append(atbat)
            self.pitches.extend(pitching_stats)
            out_ct = atbat['event_outs_ct']

    def _get_atbat(self, soup, inning_number, inning_id, pitching, out_ct):
        """
        get atbat data
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        :param pitching: pitching event list
        :param out_ct: out count
        :return: atbat result
        """
        return AtBat.row(soup, self.game, self.players, inning_number, inning_id, pitching, out_ct)

    def _get_pitch(self, soup, inning_number, inning_id, out_ct):
        """
        get pitch data
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        :param out_ct: out count
        :return: pitches result(list)
        """
        pitches = []
        for pitch in soup.find_all('pitch'):
            pitch = Pitch.row(pitch, soup, self.game, self.players, inning_number, inning_id, pitches, out_ct)
            pitches.append(pitch)
        return pitches
