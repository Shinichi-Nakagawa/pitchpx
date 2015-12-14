#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime as dt
from unittest import TestCase, main
from pitchpx.game.players import Players

__author__ = 'Shinichi Nakagawa'


class TestPlayers(TestCase):
    """
    MLBAM Players Data testing(players.xml)
    """
    XML_PLAYER_PITCHER = """
    <player id="547874" first="Hisashi" last="Iwakuma" num="18" boxname="Iwakuma" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="0" game_position="P" avg=".000" hr="0" rbi="0" wins="3" losses="2" era="4.41"/>
    """
    XML_PLAYER_BATTER = """
    <player id="572122" first="Kyle" last="Seager" num="15" boxname="Seager, K" rl="R" bats="L" position="3B" current_position="3B" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="2" game_position="3B" avg=".263" hr="16" rbi="45"/>
    """
    XML_COACH = """
    <coach position="manager" first="Lloyd" last="McClendon" id="118576" num="21"/>
    """
    XML_UMPIRE = """
    <umpire position="home" name="Jeff Nelson" id="427362" first="Jeff" last="Nelson"/>
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_player_pitcher(self):
        """
        Player data(pitcher)
        """
        soup = BeautifulSoup(TestPlayers.XML_PLAYER_PITCHER, 'lxml')
        player = Players.Player(soup.find('player'))
        self.assertEqual(player.id, '547874')
        self.assertEqual(player.first, 'Hisashi')
        self.assertEqual(player.last, 'Iwakuma')
        self.assertEqual(player.position, 'P')
        self.assertEqual(player.num, 18)
        self.assertEqual(player.box_name, 'Iwakuma')
        self.assertEqual(player.rl, 'R')
        self.assertEqual(player.bats, 'R')
        self.assertEqual(player.status, 'A')
        self.assertEqual(player.team_abbrev, 'SEA')
        self.assertEqual(player.team_id, '136')
        self.assertEqual(player.parent_team_abbrev, 'SEA')
        self.assertEqual(player.parent_team_id, '136')
        self.assertEqual(player.bat_order, 0)
        self.assertEqual(player.game_position, 'P')
        self.assertEqual(player.avg, 0.0)
        self.assertEqual(player.hr, 0)
        self.assertEqual(player.rbi, 0)
        self.assertEqual(player.wins, 3)
        self.assertEqual(player.losses, 2)
        self.assertEqual(player.era, 4.41)

    def test_player_batter(self):
        """
        Player data(batter)
        """
        soup = BeautifulSoup(TestPlayers.XML_PLAYER_BATTER, 'lxml')
        player = Players.Player(soup.find('player'))
        self.assertEqual(player.id, '572122')
        self.assertEqual(player.first, 'Kyle')
        self.assertEqual(player.last, 'Seager')
        self.assertEqual(player.position, '3B')
        self.assertEqual(player.num, 15)
        self.assertEqual(player.box_name, 'Seager, K')
        self.assertEqual(player.rl, 'R')
        self.assertEqual(player.bats, 'L')
        self.assertEqual(player.status, 'A')
        self.assertEqual(player.team_abbrev, 'SEA')
        self.assertEqual(player.team_id, '136')
        self.assertEqual(player.parent_team_abbrev, 'SEA')
        self.assertEqual(player.parent_team_id, '136')
        self.assertEqual(player.bat_order, 2)
        self.assertEqual(player.game_position, '3B')
        self.assertEqual(player.avg, 0.263)
        self.assertEqual(player.hr, 16)
        self.assertEqual(player.rbi, 45)
        self.assertEqual(player.wins, 0)
        self.assertEqual(player.losses, 0)
        self.assertEqual(player.era, 0.0)

    def test_player_coach(self):
        """
        Coach data
        """
        team = Players.Team()
        team.id = "hoge"
        team.team_type = "away"
        team.name = "name"
        soup = BeautifulSoup(TestPlayers.XML_COACH, 'lxml')
        coach = Players.Coach(soup.find('coach'), team)
        self.assertEqual(coach.id, '118576')
        self.assertEqual(coach.first, 'Lloyd')
        self.assertEqual(coach.last, 'McClendon')
        self.assertEqual(coach.position, 'manager')
        self.assertEqual(coach.num, 21)
        self.assertEqual(coach.team_id, "hoge")
        self.assertEqual(coach.team_name, "name")

    def test_player_umpire(self):
        """
        Umpire data
        """
        soup = BeautifulSoup(TestPlayers.XML_UMPIRE, 'lxml')
        umpire = Players.Umpire(soup.find('umpire'))
        self.assertEqual(umpire.id, '427362')
        self.assertEqual(umpire.first, 'Jeff')
        self.assertEqual(umpire.last, 'Nelson')
        self.assertEqual(umpire.position, 'home')
        self.assertEqual(umpire.name, 'Jeff Nelson')

if __name__ == '__main__':
    main()

