#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase, main
from pitchpx.baseball.retrosheet import RetroSheet

__author__ = 'Shinichi Nakagawa'


class TestRetroSheet(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_cd(self):
        """
        Get Event code
        """
        # Generic out
        self.assertEqual(RetroSheet.event_cd('Flyout', 'hoge fly out'), 2)
        self.assertEqual(RetroSheet.event_cd('Fly Out', 'hoge fly out'), 2)
        self.assertEqual(RetroSheet.event_cd('Sac Fly', 'hoge fly out'), 2)
        self.assertEqual(RetroSheet.event_cd('Sac Fly DP', 'hoge fly out'), 2)
        self.assertEqual(RetroSheet.event_cd('Lineout', 'hoge line out'), 2)
        self.assertEqual(RetroSheet.event_cd('Line Out', 'hoge line out'), 2)
        self.assertEqual(RetroSheet.event_cd('Bunt Lineout', 'hoge line out'), 2)
        self.assertEqual(RetroSheet.event_cd('Pop Out', 'hoge pop out'), 2)
        self.assertEqual(RetroSheet.event_cd('Pop out', 'hoge pop out'), 2)
        self.assertEqual(RetroSheet.event_cd('Bunt Pop out', 'hoge pop out'), 2)
        self.assertEqual(RetroSheet.event_cd('Groundout', 'hoge ground out'), 2)
        self.assertEqual(RetroSheet.event_cd('Ground Out', 'hoge ground out'), 2)
        self.assertEqual(RetroSheet.event_cd('Sac Bunt', 'hoge ground out'), 2)
        self.assertEqual(RetroSheet.event_cd('Bunt Groundout', 'hoge ground out'), 2)
        self.assertEqual(RetroSheet.event_cd('Grounded Into DP', 'hoge ground into dp'), 2)
        self.assertEqual(RetroSheet.event_cd('Forceout', 'hoge force out'), 2)
        self.assertEqual(RetroSheet.event_cd('Double Play', 'hoge dp'), 2)
        self.assertEqual(RetroSheet.event_cd('Triple Play', 'hoge tp'), 2)
        self.assertEqual(RetroSheet.event_cd('Sacrifice Bunt D', 'hoge bunt dp'), 2)

        # Strike out
        self.assertEqual(RetroSheet.event_cd('Strikeout', 'hoge strike out'), 3)
        self.assertEqual(RetroSheet.event_cd('Strikeout - DP', 'hoge strike out dp'), 3)

        # walk, intent walk ,hit by pitch
        self.assertEqual(RetroSheet.event_cd('Walk', 'hoge walk'), 14)
        self.assertEqual(RetroSheet.event_cd('Intent Walk', 'hoge intent walk'), 15)
        self.assertEqual(RetroSheet.event_cd('Hit By Pitch', 'hoge hit by pitch'), 16)

        # Interference
        self.assertEqual(RetroSheet.event_cd('hoge interference', 'hoge interference'), 17)
        self.assertEqual(RetroSheet.event_cd('Interference fuga', 'hoge interference'), 17)

        # Error
        self.assertEqual(RetroSheet.event_cd('hoge error', 'hoge error'), 18)
        self.assertEqual(RetroSheet.event_cd('fuga Error', 'fuga error'), 18)
        # Not Error
        self.assertEqual(RetroSheet.event_cd('error fuga', 'fuga not error'), 0)

        # Fielder's Choice
        self.assertEqual(RetroSheet.event_cd('Fielders Choice Out', 'hoge fielders choice'), 19)
        self.assertEqual(RetroSheet.event_cd('Fielders Choice', 'hoge fielders choice'), 19)

        # Single, 2B, 3B, HR
        self.assertEqual(RetroSheet.event_cd('Single', 'hoge Single'), 20)
        self.assertEqual(RetroSheet.event_cd('Double', 'hoge 2B'), 21)
        self.assertEqual(RetroSheet.event_cd('Triple', 'hoge 3B'), 22)
        self.assertEqual(RetroSheet.event_cd('Home Run', 'hoge home run'), 23)

        # Runner Out
        self.assertEqual(RetroSheet.event_cd('Runner Out', 'hoge caught stealing'), 6)
        self.assertEqual(RetroSheet.event_cd('Runner Out', 'hoge picks off'), 8)

        # Unknown Event
        self.assertEqual(RetroSheet.event_cd('bar', 'hoge picks off'), 0)
        self.assertEqual(RetroSheet.event_cd('Runner Out', 'hoge fuga'), 0)


if __name__ == '__main__':
    main()