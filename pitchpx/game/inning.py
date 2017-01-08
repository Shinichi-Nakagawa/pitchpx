#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from collections import OrderedDict
from pitchpx.mlbam_util import MlbamUtil, MlbamConst
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
        Pitch f/x fields: https://fastballs.wordpress.com/category/pitchfx-glossary/
        :param pitch: pitch object(type:Beautifulsoup)
        :param pa: At bat data for pa(dict)
        :param pitch_list: Pitching
        :param ball_tally: Ball telly
        :param strike_tally: Strike telly
        :return: {
            'retro_game_id': Retrosheet Game id
            'game_type': Game Type(S/R/F/D/L/W)
            'game_type_des': Game Type Description
            (Spring Training or Regular Season or Wild-card Game or Divisional Series or LCS or World Series)
            'st_fl': Spring Training FLAG(T or F)
            'regseason_fl': Regular Season FLAG(T or F)
            'playoff_fl': Play Off Flag(T or F)
            'local_game_time': Game Time(UTC -5)
            'game_id': Game Id
            'home_team_id': Home Team Id
            'home_team_lg': Home Team league(AL or NL)
            'away_team_id': Away Team Id
            'away_team_lg': Away Team league(AL or NL)
            'home_team_name': Home Team Name
            'away_team_name': Away Team Name
            'home_team_name_full': Home Team Name(Full Name)
            'away_team_name_full': Away Team Name(Full Name)
            'interleague_fl': Inter League Flag(T or F)
            'park_id': Park Id
            'park_name': Park Name
            'park_loc': Park Location
            'inning_number': Inning Number
            'bat_home_id': Batter Id
            'outs_ct': Out count
            'pit_mlbid': Pitcher Id
            'pit_first_name': Pitcher First Name
            'pit_last_name': Pitcher Last Name
            'pit_box_name': Pitcher Box name
            'pit_hand_cd': Pitcher Throw Hand(R or L)
            'bat_first_name': Batter First Name
            'bat_last_name': Batter Last Name
            'bat_box_name': Batter Box name
            'ab_number': At Bat Sequence Number in Game
            'start_bases': Bases(Before At Bat)
            (___, 1__, 12_, 123, etc...)
            'end_bases': Bases(After At Bat)
            (___, 1__, 12_, 123, etc...)
            'event_outs_ct': Event Out Count
            'pa_ball_ct': Plate appearance Ball count
            'pa_strike_ct': Plate appearance Strike count
            'pitch_seq': Pitch Sequence(Strike or Ball) ex: B, SSB, BBSBS etc...
            'pa_terminal_fl': Plate appearance Terminate Flag(T or F)
            'pa_event_cd': Event Code for Retrosheet http://www.retrosheet.org/datause.txt
            'pitch_res': Pitch Response(S or B or X) X = In Play
            'pitch_des': Pitch Description
            'pitch_id': Pitch Id
            'x': Point for X(inches)
            'y': Point for Y(inches)
            'start_speed': The pitch speed(MPH) at the initial point
            'end_speed': The pitch speed(MPH) at the current batters
            'sz_top': The distance in feet from the ground to the top of the current batter’s
            'sz_bot': The distance in feet from the ground to the bottom of the current batter’s
            'pfx_x': The horizontal movement, in inches, of the pitch between the release point and home plate
            'pfx_z': The vertical movement, in inches, of the pitch between the release point and home plate
            'px': The left/right distance, in feet, of the pitch from the middle of the plate as it crossed home plate
            'pz': The height of the pitch in feet as it crossed the front of home plate
            'x0': The left/right distance, in feet, of the pitch, measured at the initial point
            'y0': The distance in feet from home plate where the PITCHf/x system is set to measure the initial parameters
            'z0': The height, in feet, of the pitch, measured at the initial point
            'vx0': The velocity of the pitch, in feet per second, in three dimensions, measured at the initial point
            'vy0': The velocity of the pitch, in feet per second, in three dimensions, measured at the initial point
            'vz0': The velocity of the pitch, in feet per second, in three dimensions, measured at the initial point
            'ax': The acceleration of the pitch, in feet per second per second, in three dimensions, measured at the initial point
            'ay': The acceleration of the pitch, in feet per second per second, in three dimensions, measured at the initial point
            'az': The acceleration of the pitch, in feet per second per second, in three dimensions, measured at the initial point
            'break_y': The distance in feet from the ground to the top of the current batter’s
            'break_angle': The angle, in degrees, from vertical to the straight line path from the release point to where the pitch crossed the front of home plate, as seen from the catcher’s/umpire’s perspective
            'break_length': The measurement of the greatest distance, in inches, between the trajectory of the pitch at any point between the release point and the front of home plate
            'pitch_type': Pitch Type
            'pitch_type_seq': Pitch type Sequence, ex:FF|CU|FF
            'type_confidence': Pitch type confidence
            'zone': Pitch Zone
            'spin_dir': Pitch Spin Dir
            'spin_rate': Pitch Spin Rate
            'sv_id': Pitch in the air(From Datetime_To Datetime)
            'event_num': Event Sequence Number(atbat, pitch, action)
        }
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
        pitching['event_num'] = MlbamUtil.get_attribute_stats(pitch, 'event_num', int, -1)
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
        :return: {
            'retro_game_id': Retrosheet Game id
            'game_type': Game Type(S/R/F/D/L/W)
            'game_type_des': Game Type Description
            (Spring Training or Regular Season or Wild-card Game or Divisional Series or LCS or World Series)
            'st_fl': Spring Training FLAG(T or F)
            'regseason_fl': Regular Season FLAG(T or F)
            'playoff_fl': Play Off Flag(T or F)
            'local_game_time': Game Time(UTC -5)
            'game_id': Game Id
            'home_team_id': Home Team Id
            'home_team_lg': Home Team league(AL or NL)
            'away_team_id': Away Team Id
            'away_team_lg': Away Team league(AL or NL)
            'home_team_name': Home Team Name
            'away_team_name': Away Team Name
            'home_team_name_full': Home Team Name(Full Name)
            'away_team_name_full': Away Team Name(Full Name)
            'interleague_fl': Inter League Flag(T or F)
            'park_id': Park Id
            'park_name': Park Name
            'park_loc': Park Location
            'inning_number': Inning Number
            'bat_home_id': Batter Id
            'outs_ct': Out count
            'pit_mlbid': Pitcher Id
            'pit_first_name': Pitcher First Name
            'pit_last_name': Pitcher Last Name
            'pit_box_name': Pitcher Box name
            'pit_hand_cd': Pitcher Throw Hand(R or L)
            'bat_first_name': Batter First Name
            'bat_last_name': Batter Last Name
            'bat_box_name': Batter Box name
            'ab_number': At Bat Sequence Number in Game
            'start_bases': Bases(Before At Bat)
            (___, 1__, 12_, 123, etc...)
            'end_bases': Bases(After At Bat)
            (___, 1__, 12_, 123, etc...)
            'event_outs_ct': Event Out Count
            'ab_des': At Bat Description
            'event_tx': Event Text
            'event_cd': Event Code for Retrosheet http://www.retrosheet.org/datause.txt
            'hit_x': Hit Location(x)
            'hit_y': Hit Location(y)
            'event_num': Event Sequence Number(atbat, pitch, action)
            'home_team_runs': Score(Home)
            'away_team_runs': Score(Away)
        }
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
        atbat['event_num'] = MlbamUtil.get_attribute_stats(ab, 'event_num', int, -1)
        atbat['home_team_runs'] = MlbamUtil.get_attribute_stats(ab, 'home_team_runs', int, 0)
        atbat['away_team_runs'] = MlbamUtil.get_attribute_stats(ab, 'away_team_runs', int, 0)
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


class InningAction(object):

    DOWNLOAD_FILE_NAME = 'mlbam_action_{day}.{extension}'

    @classmethod
    def action(cls, action, game, rosters, inning_number, inning_id):
        """
        action data
        :param action: action object(type:Beautifulsoup)
        :param game: MLBAM Game object
        :param rosters: Game Rosters
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home 1:away)
        :return: {
            'retro_game_id': Retrosheet Game id
            'game_type': Game Type(S/R/F/D/L/W)
            'game_type_des': Game Type Description
            (Spring Training or Regular Season or Wild-card Game or Divisional Series or LCS or World Series)
            'st_fl': Spring Training FLAG(T or F)
            'regseason_fl': Regular Season FLAG(T or F)
            'playoff_fl': Play Off Flag(T or F)
            'local_game_time': Game Time(UTC -5)
            'game_id': Game Id
            'home_team_id': Home Team Id
            'home_team_lg': Home Team league(AL or NL)
            'away_team_id': Away Team Id
            'away_team_lg': Away Team league(AL or NL)
            'home_team_name': Home Team Name
            'away_team_name': Away Team Name
            'home_team_name_full': Home Team Name(Full Name)
            'away_team_name_full': Away Team Name(Full Name)
            'interleague_fl': Inter League Flag(T or F)
            'park_id': Park Id
            'park_name': Park Name
            'park_loc': Park Location
            'b': Ball Count
            's': Strike count
            'o': Out count
            'des': Description
            'event': Event Action
            'player_mlbid': Player Id
            'player_first_name': Player First Name
            'player_last_name': Player Last Name
            'player_box_name': Player Box Name
            'pitch': Pitch count
            'event_num': Event Sequence Number(atbat, pitch, action)
            'home_team_runs': Score(Home)
            'away_team_runs': Score(Away)
        }
        """
        player_mlbid = MlbamUtil.get_attribute_stats(action, 'player', str, MlbamConst.UNKNOWN_FULL)
        player = rosters.get(player_mlbid)
        act = OrderedDict()
        act['retro_game_id'] = game.retro_game_id
        act['year'] = game.timestamp.year
        act['month'] = game.timestamp.month
        act['day'] = game.timestamp.day
        act['st_fl'] = game.st_fl
        act['regseason_fl'] = game.regseason_fl
        act['playoff_fl'] = game.playoff_fl
        act['game_type'] = game.game_type
        act['game_type_des'] = game.game_type_des
        act['local_game_time'] = game.local_game_time
        act['game_id'] = game.game_id
        act['home_team_id'] = game.home_team_id
        act['away_team_id'] = game.away_team_id
        act['home_team_lg'] = game.home_team_lg
        act['away_team_lg'] = game.away_team_lg
        act['interleague_fl'] = game.interleague_fl
        act['park_id'] = game.park_id
        act['park_name'] = game.park_name
        act['inning_number'] = inning_number
        act['home_id'] = inning_id
        act['park_location'] = game.park_loc
        act['b'] = MlbamUtil.get_attribute_stats(action, 'b', int, 0)
        act['s'] = MlbamUtil.get_attribute_stats(action, 's', int, 0)
        act['o'] = MlbamUtil.get_attribute_stats(action, 'o', int, 0)
        act['des'] = MlbamUtil.get_attribute_stats(action, 'des', str, MlbamConst.UNKNOWN_FULL)
        act['event'] = MlbamUtil.get_attribute_stats(action, 'event', str, MlbamConst.UNKNOWN_FULL)
        act['player_mlbid'] = player_mlbid
        try:
            act['player_first_name'] = player.first
            act['player_last_name'] = player.last
            act['player_box_name'] = player.box_name
        except AttributeError as e:
            logging.error('Attribute Error(retro_game_id:{retro_game_id} player_mlbid:{player_mlbid})'
                          .format(**{'retro_game_id': game.retro_game_id, 'player_mlbid': player_mlbid}))
            act['player_first_name'] = MlbamConst.UNKNOWN_FULL
            act['player_last_name'] = MlbamConst.UNKNOWN_FULL
            act['player_box_name'] = MlbamConst.UNKNOWN_FULL
        act['pitch'] = MlbamUtil.get_attribute_stats(action, 'pitch', int, 0)
        act['event_num'] = MlbamUtil.get_attribute_stats(action, 'event_num', int, -1)
        act['home_team_runs'] = MlbamUtil.get_attribute_stats(action, 'home_team_runs', int, 0)
        act['away_team_runs'] = MlbamUtil.get_attribute_stats(action, 'away_team_runs', int, 0)
        return act


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
    actions = []

    def __init__(self, game, players):
        """
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        """
        self.game = game
        self.players = players
        self.atbats, self.pitches, self.actions = [], [], []

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
                innings._inning_actions(inning_soup, inning_number, cls.INNINGS[inning_type])
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

    def _inning_actions(self, soup, inning_number, inning_id):
        """
        Inning Actions.
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        :param inning_id: Inning Id(0:home, 1:away)
        """
        # at bat(batter box data) & pitching data
        for act in soup.find_all('action'):
            self.actions.append(InningAction.action(act, self.game, self.players.rosters, inning_number, inning_id))

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
