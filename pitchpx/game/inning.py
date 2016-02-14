#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from pitchpx.mlbam_util import MlbamUtil, MlbamConst
from pitchpx.game.game import Game
from pitchpx.baseball.retrosheet import RetroSheet

__author__ = 'Shinichi Nakagawa'


class Pitch(object):

    DOWNLOAD_FILE_NAME = 'mlbam_pitch_{day}.{extension}'

    @classmethod
    def is_pa_terminal(cls, ball_tally, strike_tally, pitch_res, event_cd):
        """
        Is PA terminal
        :param ball_tally: Ball telly
        :param strike_tally: Strike telly
        :param pitch_res: pitching result(Retrosheet format)
        :param event_cd: Event code
        :return: FLG(T or F)
        """
        if RetroSheet.is_pa_terminal(ball_tally, strike_tally, pitch_res, event_cd):
            return MlbamConst.FLG_TRUE
        return MlbamConst.FLG_FALSE

    @classmethod
    def row(cls, pitch, pa, pitch_list, ball_tally, strike_tally):
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
        pitch_type = MlbamUtil.get_attribute_stats(pitch, 'pitch_type', str, MlbamConst.UNKNOWN_SHORT)
        pitch_type_seq = [pitch['pitch_type'] for pitch in pitch_list]
        pitch_type_seq.extend([pitch_type])
        pitching = OrderedDict()
        pitching['retro_game_id'] = pa['retro_game_id']
        pitching['year'] = pa['year']
        pitching['month'] = pa['month']
        pitching['day'] = pa['day']
        pitching['st_fl'] = pa['st_fl']
        pitching['regseason_fl'] = pa['regseason_fl']
        pitching['playoff_fl'] = pa['playoff_fl']
        pitching['game_type'] = pa['game_type']
        pitching['game_type_des'] = pa['game_type_des']
        pitching['local_game_time'] = pa['local_game_time']
        pitching['game_id'] = pa['game_id']
        pitching['home_team_id'] = pa['home_team_id']
        pitching['away_team_id'] = pa['away_team_id']
        pitching['home_team_lg'] = pa['home_team_lg']
        pitching['away_team_lg'] = pa['away_team_lg']
        pitching['interleague_fl'] = pa['interleague_fl']
        pitching['park_id'] = pa['park_id']
        pitching['park_name'] = pa['park_name']
        pitching['park_location'] = pa['park_location']
        pitching['inning_number'] = pa['inning_number']
        pitching['bat_home_id'] = pa['bat_home_id']
        pitching['outs_ct'] = pa['outs_ct']
        pitching['pit_mlbid'] = pa['pit_mlbid']
        pitching['pit_first_name'] = pa['pit_first_name']
        pitching['pit_last_name'] = pa['pit_last_name']
        pitching['pit_box_name'] = pa['pit_box_name']
        pitching['pit_hand_cd'] = pa['pit_hand_cd']
        pitching['bat_mlbid'] = pa['bat_mlbid']
        pitching['bat_first_name'] = pa['bat_first_name']
        pitching['bat_last_name'] = pa['bat_last_name']
        pitching['bat_box_name'] = pa['bat_box_name']
        pitching['bat_hand_cd'] = pa['bat_hand_cd']
        pitching['ab_number'] = pa['ab_number']
        pitching['start_bases'] = pa['start_bases']
        pitching['end_bases'] = pa['end_bases']
        pitching['event_outs_ct'] = pa['event_outs_ct']
        pitching['pa_ball_ct'] = ball_tally
        pitching['pa_strike_ct'] = strike_tally
        pitching['pitch_seq'] = ''.join(pitch_seq)
        pitching['pa_terminal_fl'] = cls.is_pa_terminal(ball_tally, strike_tally, pitch_res, pa['event_cd'])
        pitching['pa_event_cd'] = pa['event_cd']
        pitching['pitch_res'] = pitch_res
        pitching['pitch_des'] = MlbamUtil.get_attribute_stats(pitch, 'des', str, MlbamConst.UNKNOWN_FULL)
        pitching['pitch_id'] = MlbamUtil.get_attribute_stats(pitch, 'id', int, None)
        pitching['x'] = MlbamUtil.get_attribute_stats(pitch, 'x', float, None)
        pitching['y'] = MlbamUtil.get_attribute_stats(pitch, 'y', float, None)
        pitching['start_speed'] = MlbamUtil.get_attribute_stats(pitch, 'start_speed', float, None)
        pitching['end_speed'] = MlbamUtil.get_attribute_stats(pitch, 'end_speed', float, None)
        pitching['sz_top'] = MlbamUtil.get_attribute_stats(pitch, 'sz_top', float, None)
        pitching['sz_bot'] = MlbamUtil.get_attribute_stats(pitch, 'sz_bot', float, None)
        pitching['pfx_x'] = MlbamUtil.get_attribute_stats(pitch, 'pfx_x', float, None)
        pitching['pfx_z'] = MlbamUtil.get_attribute_stats(pitch, 'pfx_z', float, None)
        pitching['px'] = MlbamUtil.get_attribute_stats(pitch, 'px', float, None)
        pitching['pz'] = MlbamUtil.get_attribute_stats(pitch, 'pz', float, None)
        pitching['x0'] = MlbamUtil.get_attribute_stats(pitch, 'x0', float, None)
        pitching['y0'] = MlbamUtil.get_attribute_stats(pitch, 'y0', float, None)
        pitching['z0'] = MlbamUtil.get_attribute_stats(pitch, 'z0', float, None)
        pitching['vx0'] = MlbamUtil.get_attribute_stats(pitch, 'vx0', float, None)
        pitching['vy0'] = MlbamUtil.get_attribute_stats(pitch, 'vy0', float, None)
        pitching['vz0'] = MlbamUtil.get_attribute_stats(pitch, 'vz0', float, None)
        pitching['ax'] = MlbamUtil.get_attribute_stats(pitch, 'ax', float, None)
        pitching['ay'] = MlbamUtil.get_attribute_stats(pitch, 'ay', float, None)
        pitching['az'] = MlbamUtil.get_attribute_stats(pitch, 'az', float, None)
        pitching['break_y'] = MlbamUtil.get_attribute_stats(pitch, 'break_y', float, None)
        pitching['break_angle'] = MlbamUtil.get_attribute_stats(pitch, 'break_angle', float, None)
        pitching['break_length'] = MlbamUtil.get_attribute_stats(pitch, 'break_length', float, None)
        pitching['pitch_type'] = pitch_type
        pitching['pitch_type_seq'] = '|'.join(pitch_type_seq)
        pitching['type_confidence'] = MlbamUtil.get_attribute_stats(pitch, 'type_confidence', float, None)
        pitching['zone'] = MlbamUtil.get_attribute_stats(pitch, 'zone', float, None)
        pitching['spin_dir'] = MlbamUtil.get_attribute_stats(pitch, 'spin_dir', float, None)
        pitching['spin_rate'] = MlbamUtil.get_attribute_stats(pitch, 'spin_rate', float, None)
        pitching['sv_id'] = MlbamUtil.get_attribute_stats(pitch, 'sv_id', str, None)
        return pitching


class AtBat(object):

    DOWNLOAD_FILE_NAME = 'mlbam_atbat_{day}.{extension}'

    @classmethod
    def _get_bases(cls, ab):
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
    def pa(cls, ab, game, rosters, inning_number, inning_id, out_ct, hit_location):
        """
        plate appearance data
        :param ab: at bat object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param rosters: Game Rosters
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home 1:away)
        :param pitch_list: Pitching
        :param out_ct: out count
        :param hit_location: Hitlocation data(dict)
        :return: pa value(dict)
        """
        ab_des = MlbamUtil.get_attribute_stats(ab, 'des', str, MlbamConst.UNKNOWN_FULL)
        event_tx = MlbamUtil.get_attribute_stats(ab, 'event', str, MlbamConst.UNKNOWN_FULL)
        event_cd = RetroSheet.event_cd(event_tx, ab_des)
        event_outs_ct = MlbamUtil.get_attribute_stats(ab, 'o', int, 0)
        start_bases, end_bases = cls._get_bases(ab)
        pit_mlbid = MlbamUtil.get_attribute_stats(ab, 'pitcher', str, MlbamConst.UNKNOWN_FULL)
        bat_mlbid = MlbamUtil.get_attribute_stats(ab, 'batter', str, MlbamConst.UNKNOWN_FULL)
        pit_player = rosters.get(pit_mlbid)
        bat_player = rosters.get(bat_mlbid)
        location_key = Inning.HITLOCATION_KEY_FORMAT.format(
            inning=inning_number,
            des=event_tx,
            pitcher=pit_mlbid,
            batter=bat_mlbid,
        )
        location = hit_location.get(location_key, {})
        atbat = OrderedDict()
        atbat['retro_game_id'] = game.retro_game_id
        atbat['year'] = game.timestamp.year
        atbat['month'] = game.timestamp.month
        atbat['day'] = game.timestamp.day
        atbat['st_fl'] = game.st_fl
        atbat['regseason_fl'] = game.regseason_fl
        atbat['playoff_fl'] = game.playoff_fl
        atbat['game_type'] = game.game_type
        atbat['game_type_des'] = game.game_type_des
        atbat['local_game_time'] = game.local_game_time
        atbat['game_id'] = game.game_id
        atbat['home_team_id'] = game.home_team_id
        atbat['away_team_id'] = game.away_team_id
        atbat['home_team_lg'] = game.home_team_lg
        atbat['away_team_lg'] = game.away_team_lg
        atbat['interleague_fl'] = game.interleague_fl
        atbat['park_id'] = game.park_id
        atbat['park_name'] = game.park_name
        atbat['park_location'] = game.park_loc
        atbat['inning_number'] = inning_number
        atbat['bat_home_id'] = inning_id
        atbat['outs_ct'] = out_ct
        atbat['pit_mlbid'] = pit_mlbid
        atbat['pit_first_name'] = pit_player.first
        atbat['pit_last_name'] = pit_player.last
        atbat['pit_box_name'] = pit_player.box_name
        atbat['pit_hand_cd'] = MlbamUtil.get_attribute_stats(ab, 'p_throws', str, MlbamConst.UNKNOWN_FULL)
        atbat['bat_mlbid'] = bat_mlbid
        atbat['bat_first_name'] = bat_player.first
        atbat['bat_last_name'] = bat_player.last
        atbat['bat_box_name'] = bat_player.box_name
        atbat['bat_hand_cd'] = MlbamUtil.get_attribute_stats(ab, 'stand', str, MlbamConst.UNKNOWN_FULL)
        atbat['ab_number'] = MlbamUtil.get_attribute_stats(ab, 'num', int, None)
        atbat['start_bases'] = start_bases
        atbat['end_bases'] = end_bases
        atbat['event_outs_ct'] = event_outs_ct
        atbat['ab_des'] = ab_des
        atbat['event_tx'] = event_tx
        atbat['event_cd'] = event_cd
        atbat['hit_x'] = location.get('hit_x', None)
        atbat['hit_y'] = location.get('hit_y', None)
        return atbat

    @classmethod
    def result(cls, ab, pa, pitch_list):
        """
        At Bat Result
        :param ab: at bat object(type:Beautifulsoup)
        :param pa: atbat data for plate appearance
        :param pitch_list: Pitching data
        :return: pa result value(dict)
        """
        atbat = OrderedDict()
        atbat['ball_ct'] = MlbamUtil.get_attribute_stats(ab, 'b', int, None)
        atbat['strike_ct'] = MlbamUtil.get_attribute_stats(ab, 's', int, None)
        atbat['pitch_seq'] = ''.join([pitch['pitch_res'] for pitch in pitch_list])
        atbat['pitch_type_seq'] = '|'.join([pitch['pitch_type'] for pitch in pitch_list])
        atbat['battedball_cd'] = RetroSheet.battedball_cd(pa['event_cd'], pa['event_tx'], pa['ab_des'])
        return atbat


class Inning(object):

    DIRECTORY = 'inning'
    FILENAME_PATTERN = 'inning_\d*.xml'
    FILENAME_INNING_HIT = 'inning_hit.xml'
    HITLOCATION_KEY_FORMAT = '{inning}_{des}_{pitcher}_{batter}'
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
        self.atbats, self.pitches = [], []

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
        # hit location data
        hit_location = cls._read_hit_chart_data(
                MlbamUtil.find_xml('/'.join([base_url, cls.FILENAME_INNING_HIT]), markup)
        )

        # create for atbat & pitch data
        for inning in MlbamUtil.find_xml_all(base_url, markup, cls.TAG, cls.FILENAME_PATTERN):
            soup = MlbamUtil.find_xml("/".join([base_url, inning.get_text().strip()]), markup)
            inning_number = int(soup.inning['num'])
            for inning_type in cls.INNINGS.keys():
                inning_soup = soup.inning.find(inning_type)
                if inning_soup is None:
                    break
                innings._inning_events(inning_soup, inning_number, cls.INNINGS[inning_type], hit_location)
        return innings

    @classmethod
    def _read_hit_chart_data(cls, soup):
        """

        :param soup: Beautifulsoup object
        :return: dictionary data
        """
        hit_chart = {}
        for hip in soup.find_all('hip'):
            key = cls.HITLOCATION_KEY_FORMAT.format(
                inning=MlbamUtil.get_attribute_stats(hip, 'inning', int),
                des=MlbamUtil.get_attribute_stats(hip, 'des', str),
                pitcher=MlbamUtil.get_attribute_stats(hip, 'pitcher', str),
                batter=MlbamUtil.get_attribute_stats(hip, 'batter', str),
            )
            hit_chart[key] = {
                'hit_x': MlbamUtil.get_attribute_stats(hip, 'x', float, None),
                'hit_y': MlbamUtil.get_attribute_stats(hip, 'y', float, None),
            }
        return hit_chart

    def _inning_events(self, soup, inning_number, inning_id, hit_location):
        """
        Inning Events.
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        :param hit_location: Hitlocation data(dict)
        """
        # at bat(batter box data) & pitching data
        out_ct = 0
        for ab in soup.find_all('atbat'):
            # plate appearance data(pa)
            at_bat = AtBat.pa(ab, self.game, self.players.rosters, inning_number, inning_id, out_ct, hit_location)
            # pitching data
            pitching_stats = self._get_pitch(ab, at_bat)
            # at bat(pa result)
            pa_result = AtBat.result(ab, at_bat, pitching_stats)
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
