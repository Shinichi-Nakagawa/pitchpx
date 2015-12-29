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

    def test_battedball_cd(self):
        """
        Get Battedball code
        """
        # Generic out
        self.assertEqual(RetroSheet.battedball_cd(2, 'Flyout', 'hoge fly out'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Fly Out', 'hoge fly out'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sac Fly', 'hoge fly out'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sac Fly DP', 'hoge fly out'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Lineout', 'hoge line out'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Line Out', 'hoge line out'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Bunt Lineout', 'hoge line out'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Pop Out', 'hoge pop out'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Pop out', 'hoge pop out'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Bunt Pop out', 'hoge pop out'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Groundout', 'hoge ground out'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Ground Out', 'hoge ground out'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sac Bunt', 'hoge ground out'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Bunt Groundout', 'hoge ground out'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Grounded Into DP', 'hoge ground into dp'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Forceout', 'hoge force out grounds'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Forceout', 'hoge force out lines'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Forceout', 'hoge force out flies'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Forceout', 'hoge force out pops'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Forceout', 'hoge force out'), '')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Double Play', 'hoge dp grounds'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Double Play', 'hoge dp lines'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Double Play', 'hoge dp flies'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Double Play', 'hoge dp pops'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Double Play', 'hoge dp'), '')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Triple Play', 'hoge tp grounds'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Triple Play', 'hoge tp lines'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Triple Play', 'hoge tp flies'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Triple Play', 'hoge tp pops'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Triple Play', 'hoge tp'), '')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sacrifice Bunt D', 'hoge bunt dp grounds'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sacrifice Bunt D', 'hoge bunt dp lines'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sacrifice Bunt D', 'hoge bunt dp flies'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sacrifice Bunt D', 'hoge bunt dp pops'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(2, 'Sacrifice Bunt D', 'hoge bunt dp'), '')

        # Strike out
        self.assertEqual(RetroSheet.battedball_cd(3, 'Strikeout', 'hoge strike out'), '')
        self.assertEqual(RetroSheet.battedball_cd(3, 'Strikeout - DP', 'hoge strike out dp'), '')

        # walk, intent walk ,hit by pitch
        self.assertEqual(RetroSheet.battedball_cd(14, 'Walk', 'hoge walk'), '')
        self.assertEqual(RetroSheet.battedball_cd(15, 'Intent Walk', 'hoge intent walk'), '')
        self.assertEqual(RetroSheet.battedball_cd(16, 'Hit By Pitch', 'hoge hit by pitch'), '')

        # Interference
        self.assertEqual(RetroSheet.battedball_cd(17, 'hoge interference', 'hoge interference'), '')
        self.assertEqual(RetroSheet.battedball_cd(17, 'Interference fuga', 'hoge interference'), '')

        # Error
        self.assertEqual(RetroSheet.battedball_cd(18, 'hoge error', 'hoge error'), '')
        self.assertEqual(RetroSheet.battedball_cd(18, 'fuga Error', 'fuga error'), '')
        # Not Error
        self.assertEqual(RetroSheet.battedball_cd(0, 'error fuga', 'fuga not error'), '')

        # Fielder's Choice
        self.assertEqual(RetroSheet.battedball_cd(19, 'Fielders Choice Out', 'hoge fielders choice'), '')
        self.assertEqual(RetroSheet.battedball_cd(19, 'Fielders Choice', 'hoge fielders choice'), '')

        # Single, 2B, 3B, HR
        self.assertEqual(RetroSheet.battedball_cd(20, 'Single', 'hoge Single on a line drive to fuga'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(20, 'Single', 'hoge Single fly ball to fuga'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(20, 'Single', 'hoge Single ground ball to fuga'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(20, 'Single', 'hoge Single pop up to fuga'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(20, 'Single', 'hoge Single'), '')
        self.assertEqual(RetroSheet.battedball_cd(21, 'Double', 'hoge 2B on a line drive to fuga'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(21, 'Double', 'hoge 2B fly ball to fuga'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(21, 'Double', 'hoge 2B ground ball to fuga'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(21, 'Double', 'hoge 2B pop up to fuga'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(21, 'Double', 'hoge 2B'), '')
        self.assertEqual(RetroSheet.battedball_cd(22, 'Triple', 'hoge 3B on a line drive to fuga'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(22, 'Triple', 'hoge 3B fly ball to fuga'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(22, 'Triple', 'hoge 3B ground ball to fuga'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(22, 'Triple', 'hoge 3B pop up to fuga'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(22, 'Triple', 'hoge 3B'), '')
        self.assertEqual(RetroSheet.battedball_cd(23, 'Home Run', 'hoge 3B on a line drive to fuga'), 'L')
        self.assertEqual(RetroSheet.battedball_cd(23, 'Home Run', 'hoge 3B fly ball to fuga'), 'F')
        self.assertEqual(RetroSheet.battedball_cd(23, 'Home Run', 'hoge 3B ground ball to fuga'), 'G')
        self.assertEqual(RetroSheet.battedball_cd(23, 'Home Run', 'hoge 3B pop up to fuga'), 'P')
        self.assertEqual(RetroSheet.battedball_cd(23, 'Home Run', 'hoge 3B'), '')

        # Runner Out
        self.assertEqual(RetroSheet.battedball_cd(6, 'Runner Out', 'hoge caught stealing'), '')
        self.assertEqual(RetroSheet.battedball_cd(8, 'Runner Out', 'hoge picks off'), '')

        # Unknown Event
        self.assertEqual(RetroSheet.battedball_cd(0, 'bar', 'hoge picks off'), '')
        self.assertEqual(RetroSheet.battedball_cd(0, 'Runner Out', 'hoge fuga'), '')


if __name__ == '__main__':
    main()