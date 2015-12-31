#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime as dt
from bs4 import BeautifulSoup
from unittest import TestCase, main
from pitchpx.game.inning import Inning
from pitchpx.game.game import Game
from pitchpx.game.players import Players

__author__ = 'Shinichi Nakagawa'


class TestInning(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        url = 'http://gd2.mlb.com/components/game/mlb/year_2015/month_08/day_12/gid_2015_08_12_balmlb_seamlb_1/'
        markup = 'lxml'
        timestamp = dt.strptime('2015-08-12', '%Y-%m-%d')
        game_number = 0
        game = Game.read_xml(url, markup, timestamp, game_number)
        players = Players.read_xml(url, markup)
        inning = Inning.read_xml(url, markup, game, players)


if __name__ == '__main__':
    main()
