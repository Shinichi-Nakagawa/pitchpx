#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime as dt
from unittest import TestCase, main
from pitchpx.game.game import Game

__author__ = 'Shinichi Nakagawa'


class TestGame(TestCase):
    """
    MLBAM Game Data testing(game.xml)
    """
    GAME_XML = """
    <game type="R" local_game_time="12:40" game_pk="415346" game_time_et="03:40 PM" gameday_sw="P">
	    <team type="home" code="sea" file_code="sea" abbrev="SEA" id="136" name="Seattle" name_full="Seattle Mariners" name_brief="Mariners" w="54" l="61" division_id="200" league_id="103" league="AL"/>
	    <team type="away" code="bal" file_code="bal" abbrev="BAL" id="110" name="Baltimore" name_full="Baltimore Orioles" name_brief="Orioles" w="57" l="56" division_id="201" league_id="103" league="AL"/>
	    <stadium id="680" name="Safeco Field" venue_w_chan_loc="USWA0395" location="Seattle, WA"/>
    """
    DUMMY_XML = """
    <game>
	    <hoge type="home" code="sea" file_code="sea" abbrev="SEA" id="136" name="Seattle" name_full="Seattle Mariners" name_brief="Mariners" w="54" l="61" division_id="200" league_id="103" league="AL"/>
	    <hoge type="away" code="bal" file_code="bal" abbrev="BAL" id="110" name="Baltimore" name_full="Baltimore Orioles" name_brief="Orioles" w="57" l="56" division_id="201" league_id="103" league="AL"/>
	    <fuga id="680" name="Safeco Field" venue_w_chan_loc="USWA0395" location="Seattle, WA"/>
    </game>
    """

    def setUp(self):
        self.game = BeautifulSoup(TestGame.GAME_XML, 'lxml')
        self.dummy = BeautifulSoup(TestGame.DUMMY_XML, 'lxml')

    def tearDown(self):
        self.game = None
        self.dummy = None

    def test_row(self):
        """
        Game Object Data(row data)
        """
        game = Game._generate_game_object(self.game, dt.strptime('2015-08-13', '%Y-%m-%d'), 2)
        row = game.row()

        # Base Data
        self.assertEqual(row['game_type'], 'R')
        self.assertEqual(row['game_type_des'], 'Regular Season')
        self.assertEqual(row['st_fl'], 'F')
        self.assertEqual(row['regseason_fl'], 'T')
        self.assertEqual(row['local_game_time'], '12:40')
        self.assertEqual(row['game_id'], '415346')

        # Team Data
        self.assertEqual(row['home_team_id'], 'sea')
        self.assertEqual(row['away_team_id'], 'bal')
        self.assertEqual(row['home_team_lg'], 'AL')
        self.assertEqual(row['away_team_lg'], 'AL')
        self.assertEqual(row['home_team_name'], 'Seattle')
        self.assertEqual(row['away_team_name'], 'Baltimore')
        self.assertEqual(row['home_team_name_full'], 'Seattle Mariners')
        self.assertEqual(row['away_team_name_full'], 'Baltimore Orioles')

        # Stadium Data
        self.assertEqual(row['park_id'], '680')
        self.assertEqual(row['park_name'], 'Safeco Field')
        self.assertEqual(row['park_loc'], 'Seattle, WA')

        # Retro ID
        self.assertEqual(row['retro_game_id'], 'SEA201508131')

    def test_generate_game_object(self):
        """
        Game Object Data
        """
        game = Game._generate_game_object(self.game, dt.strptime('2015-08-12', '%Y-%m-%d'), 1)

        # Base Data
        self.assertEqual(game.game_type, 'R')
        self.assertEqual(game.game_type_des, 'Regular Season')
        self.assertEqual(game.st_fl, 'F')
        self.assertEqual(game.regseason_fl, 'T')
        self.assertEqual(game.local_game_time, '12:40')
        self.assertEqual(game.game_id, '415346')

        # Team Data
        self.assertEqual(game.home_team_id, 'sea')
        self.assertEqual(game.away_team_id, 'bal')
        self.assertEqual(game.home_team_lg, 'AL')
        self.assertEqual(game.away_team_lg, 'AL')
        self.assertEqual(game.home_team_name, 'Seattle')
        self.assertEqual(game.away_team_name, 'Baltimore')
        self.assertEqual(game.home_team_name_full, 'Seattle Mariners')
        self.assertEqual(game.away_team_name_full, 'Baltimore Orioles')

        # Stadium Data
        self.assertEqual(game.park_id, '680')
        self.assertEqual(game.park_name, 'Safeco Field')
        self.assertEqual(game.park_loc, 'Seattle, WA')

        # Retro ID
        self.assertEqual(game.retro_game_id, 'SEA201508120')

    def test_spring_training(self):
        """
        Spring Training Data
        """
        self.assertEqual(Game._get_game_type_des('S'), 'Spring Training')
        self.assertEqual(Game._get_st_fl('S'), 'T')
        self.assertEqual(Game._get_regseason_fl('S'), 'F')
        self.assertEqual(Game._get_playoff_fl('S'), 'F')

    def test_regular_season(self):
        """
        Regular Season Data
        """
        self.assertEqual(Game._get_game_type_des('R'), 'Regular Season')
        self.assertEqual(Game._get_st_fl('R'), 'F')
        self.assertEqual(Game._get_regseason_fl('R'), 'T')
        self.assertEqual(Game._get_playoff_fl('R'), 'F')

    def test_wild_card_game(self):
        """
        Wild-card Game Data
        """
        self.assertEqual(Game._get_game_type_des('F'), 'Wild-card Game')
        self.assertEqual(Game._get_st_fl('F'), 'F')
        self.assertEqual(Game._get_regseason_fl('F'), 'F')
        self.assertEqual(Game._get_playoff_fl('F'), 'T')

    def test_divisional_series(self):
        """
        Divisional Series Data
        """
        self.assertEqual(Game._get_game_type_des('D'), 'Divisional Series')
        self.assertEqual(Game._get_st_fl('D'), 'F')
        self.assertEqual(Game._get_regseason_fl('D'), 'F')
        self.assertEqual(Game._get_playoff_fl('D'), 'T')

    def test_world_series(self):
        """
        World Series Data
        """
        self.assertEqual(Game._get_game_type_des('W'), 'World Series')
        self.assertEqual(Game._get_st_fl('W'), 'F')
        self.assertEqual(Game._get_regseason_fl('W'), 'F')
        self.assertEqual(Game._get_playoff_fl('W'), 'T')

    def test_game_type_unknown(self):
        """
        Unknow Game Type
        """
        self.assertEqual(Game._get_game_type_des('U'), 'Unknown')
        self.assertEqual(Game._get_st_fl('U'), 'F')
        self.assertEqual(Game._get_regseason_fl('U'), 'F')
        self.assertEqual(Game._get_playoff_fl('U'), 'F')

    def test_league_champion_ship(self):
        """
        League Champion Ship Data
        """
        self.assertEqual(Game._get_game_type_des('L'), 'LCS')
        self.assertEqual(Game._get_st_fl('L'), 'F')
        self.assertEqual(Game._get_regseason_fl('L'), 'F')
        self.assertEqual(Game._get_playoff_fl('L'), 'T')

    def test_interleague(self):
        """
        inter league
        """
        self.assertEqual(Game._get_interleague_fl('AL', 'NL'), 'T')

    def test_not_interleague(self):
        """
        inter league(not)
        """
        self.assertEqual(Game._get_interleague_fl('AL', 'AL'), 'F')
        self.assertEqual(Game._get_interleague_fl('NL', 'NL'), 'F')

    def test_unknown_interleague(self):
        """
        inter league(unknown)
        """
        self.assertEqual(Game._get_interleague_fl('AL', 'U'), 'U')
        self.assertEqual(Game._get_interleague_fl('U', 'NL'), 'U')

    def test_team_attributes_exists(self):
        """
        Team attributes Data
        """
        self.assertEqual(Game._get_team_attribute(self.game, 'home', 'code'), 'sea')
        self.assertEqual(Game._get_team_attribute(self.game, 'away', 'code'), 'bal')
        self.assertEqual(Game._get_team_attribute(self.game, 'home', 'league'), 'AL')
        self.assertEqual(Game._get_team_attribute(self.game, 'away', 'league'), 'AL')
        self.assertEqual(Game._get_team_attribute(self.game, 'home', 'name'), 'Seattle')
        self.assertEqual(Game._get_team_attribute(self.game, 'away', 'name'), 'Baltimore')
        self.assertEqual(Game._get_team_attribute(self.game, 'home', 'name_full'), 'Seattle Mariners')
        self.assertEqual(Game._get_team_attribute(self.game, 'away', 'name_full'), 'Baltimore Orioles')

    def test_team_stadium_exists(self):
        """
        Stadium Data
        """
        self.assertEqual(Game._get_stadium_attribute(self.game, 'id'), '680')
        self.assertEqual(Game._get_stadium_attribute(self.game, 'name'), 'Safeco Field')
        self.assertEqual(Game._get_stadium_attribute(self.game, 'location'), 'Seattle, WA')

    def test_team_attributes_not_exists(self):
        """
        Team attributes Data(not exists)
        """
        self.assertEqual(Game._get_team_attribute(self.dummy, 'home', 'code'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'away', 'code'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'home', 'league'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'away', 'league'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'home', 'name'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'away', 'name'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'home', 'name_full'), 'Unknown')
        self.assertEqual(Game._get_team_attribute(self.dummy, 'home', 'name_full'), 'Unknown')

    def test_team_stadium_not_exists(self):
        """
        Stadium Data(not exists)
        """
        self.assertEqual(Game._get_stadium_attribute(self.dummy, 'id'), 'Unknown')
        self.assertEqual(Game._get_stadium_attribute(self.dummy, 'name'), 'Unknown')
        self.assertEqual(Game._get_stadium_attribute(self.dummy, 'location'), 'Unknown')

    def test_retro_id(self):
        """
        Retro ID
        """
        self.assertEqual(Game._get_retro_id('SEA', dt.strptime('2015-08-12', '%Y-%m-%d'), 1), 'SEA201508120')
        self.assertEqual(Game._get_retro_id('OAK', dt.strptime('2015-04-03', '%Y-%m-%d'), 2), 'OAK201504031')
        self.assertEqual(Game._get_retro_id('MIA', dt.strptime('2015-10-01', '%Y-%m-%d'), 3), 'MIA201510012')

if __name__ == '__main__':
    main()

