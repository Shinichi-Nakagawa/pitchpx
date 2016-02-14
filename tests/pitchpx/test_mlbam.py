#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase, main
from pitchpx.mlbam import MlbAm

__author__ = 'Shinichi Nakagawa'


class TestMlbAm(TestCase):
    """
    MLBAM scrape class testing
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_game_number(self):
        """
        Game number Test
        """
        self.assertEqual(MlbAm._get_game_number('gid_2015_08_12_balmlb_seamlb_1/'), 1)
        self.assertEqual(MlbAm._get_game_number('gid_2015_05_06_arimlb_colmlb_1/'), 1)
        self.assertEqual(MlbAm._get_game_number('gid_2015_05_06_arimlb_colmlb_2/'), 2)


if __name__ == '__main__':
    main()