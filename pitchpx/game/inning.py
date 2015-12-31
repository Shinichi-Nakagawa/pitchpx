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
    def row(cls, pitch, pa: dict, pitch_list: list, ball_tally: int, strike_tally: int) -> dict:
        """
        Pitching Result
        :param pitch: pitch object(type:Beautifulsoup)
        :param pa: At bat data for pa(dict)
        :param pitch_list: Pitching
        :param ball_tally: Ball telly
        :param strike_tally: Strike telly
        :return: row value(dict)
        """
        pitch_res = MlbamUtil.get_attribute_stats(pitch, 'type', str, MlbamConst.UNKNOWN_FULL)
        pitch_seq = [pitch['pitch_res'] for pitch in pitch_list]
        pitch_seq.extend([pitch_res])
        pitch_type = MlbamUtil.get_attribute_stats(pitch, 'pitch_type', str, None)
        pitch_type_seq = [pitch['pitch_type'] for pitch in pitch_list]
        pitch_type_seq.extend([pitch_type])
        return {
            'retro_game_id': pa['retro_game_id'],
            'year': pa['year'],
            'month': pa['month'],
            'day': pa['day'],
            'st_fl': pa['st_fl'],
            'regseason_fl': pa['regseason_fl'],
            'playoff_fl': pa['playoff_fl'],
            'game_type': pa['game_type'],
            'game_type_des': pa['game_type_des'],
            'local_game_time': pa['local_game_time'],
            'game_id': pa['game_id'],
            'home_team_id': pa['home_team_id'],
            'away_team_id': pa['away_team_id'],
            'home_team_lg': pa['home_team_lg'],
            'away_team_lg': pa['away_team_lg'],
            'interleague_fl': pa['interleague_fl'],
            'park_id': pa['park_id'],
            'park_name': pa['park_name'],
            'park_location': pa['park_location'],
            'inning_number': pa['inning_number'],
            'bat_home_id': pa['bat_home_id'],
            'outs_ct': pa['outs_ct'],
            'pit_mlbid': pa['pit_mlbid'],
            'pit_hand_cd': pa['pit_hand_cd'],
            'bat_mlbid': pa['bat_mlbid'],
            'bat_hand_cd': pa['bat_hand_cd'],
            'ab_number': pa['ab_number'],
            'start_bases': pa['start_bases'],
            'end_bases': pa['end_bases'],
            'event_outs_ct': pa['event_outs_ct'],
            'pa_ball_ct': ball_tally,
            'pa_strike_ct': strike_tally,
            'pitch_seq': ''.join(pitch_seq),
            'pa_terminal_fl': None,  # TODO 後で
            'pa_event_cd': None,  # TODO 後で
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
    def _get_bases(cls, ab) -> str:
        """
        Start Bases & End Bases
        :param ab: at bat object(type:Beautifulsoup)
        :param attribute_name: attribute name
        :return: start base, end base
        """
        start_bases, end_bases = [], []
        for base in ('1B', '2B', '3B'):
            if ab.find('runner', start=base):
                start_bases.append(base[0:1])
            else:
                start_bases.append('_')
            if ab.find('runner', end=base):
                end_bases.append(base[0:1])
            else:
                end_bases.append('_')
        return ''.join(start_bases), ''.join(end_bases)

    @classmethod
    def pa(cls, ab, game: Game, players: Players, inning_number: int, inning_id: int, out_ct: int) -> dict:
        """
        plate appearance data
        :param ab: at bat object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home 1:away)
        :param pitch_list: Pitching
        :param out_ct: out count
        :return: pa value(dict)
        """
        event_outs_ct = MlbamUtil.get_attribute_stats(ab, 'o', int, 0)
        start_bases, end_bases = cls._get_bases(ab)
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
            'pit_mlbid': MlbamUtil.get_attribute_stats(ab, 'pitcher', str, MlbamConst.UNKNOWN_FULL),
            'pit_hand_cd': MlbamUtil.get_attribute_stats(ab, 'p_throws', str, MlbamConst.UNKNOWN_FULL),
            'bat_mlbid': MlbamUtil.get_attribute_stats(ab, 'batter', str, MlbamConst.UNKNOWN_FULL),
            'bat_hand_cd': MlbamUtil.get_attribute_stats(ab, 'stand', str, MlbamConst.UNKNOWN_FULL),
            'ab_number': MlbamUtil.get_attribute_stats(ab, 'num', int, None),
            'start_bases': start_bases,
            'end_bases': end_bases,
            'event_outs_ct': event_outs_ct,
        }

    @classmethod
    def result(cls, ab, pitch_list):
        """
        At Bat Result
        :param ab: at bat object(type:Beautifulsoup)
        :param pitch_list: Pitching data
        :return: pa result value(dict)
        """
        ab_des = MlbamUtil.get_attribute_stats(ab, 'des', str, MlbamConst.UNKNOWN_FULL)
        event_tx = MlbamUtil.get_attribute_stats(ab, 'event', str, MlbamConst.UNKNOWN_FULL)
        event_cd = RetroSheet.event_cd(event_tx, ab_des)
        battedball_cd = RetroSheet.battedball_cd(event_cd, event_tx, ab_des)
        return {
            'ball_ct': MlbamUtil.get_attribute_stats(ab, 'b', int, None),
            'strike_ct': MlbamUtil.get_attribute_stats(ab, 's', int, None),
            'pitch_seq': ''.join([pitch['pitch_res'] for pitch in pitch_list]),
            'pitch_type_seq': '|'.join([pitch['pitch_type'] for pitch in pitch_list]),
            'ab_des': ab_des,
            'event_tx': event_tx,
            'event_cd': event_cd,
            'battedball_cd': battedball_cd,
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
            # plate appearance data(pa)
            at_bat = AtBat.pa(ab, self.game, self.players, inning_number, inning_id, out_ct)
            # pitching data
            pitching_stats = self._get_pitch(ab, at_bat)
            # at bat(pa result)
            pa_result = AtBat.result(ab, pitching_stats)
            at_bat.update(pa_result)
            self.atbats.append(at_bat)
            self.pitches.extend(pitching_stats)
            # out count
            out_ct = at_bat['event_outs_ct']

    def _get_pitch(self, soup, pa):
        """
        get pitch data
        :param soup: Beautifulsoup object
        :param pa: atbat data for plate appearance
        :return: pitches result(list)
        """
        pitches = []
        ball_tally, strike_tally = 0, 0
        for pitch in soup.find_all('pitch'):
            # pitching result
            pitch = Pitch.row(pitch, pa, pitches, ball_tally, strike_tally)
            pitches.append(pitch)
            # ball count
            ball_tally, strike_tally = RetroSheet.ball_count(ball_tally, strike_tally, pitch['pitch_res'])
        return pitches
