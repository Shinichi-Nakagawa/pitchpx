#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from pitchpx.game.game import Game

__author__ = 'Shinichi Nakagawa'


class TestGame(TestCase):
    """
    MLBAM Game Data testing(game.xml)
    """

    def setUp(self):
        pass

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

    def tearDown(self):
        pass

if __name__ == '__main__':
    main()

