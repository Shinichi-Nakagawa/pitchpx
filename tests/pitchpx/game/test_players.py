#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
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
    XML_COACH_NOT_NUMBER = """
    <coach position="baserunning/outfield_and_first_base_coach" first="Doug" last="Sisson" id="579474" num=""/>
    """
    XML_UMPIRE = """
    <umpire position="home" name="Jeff Nelson" id="427362" first="Jeff" last="Nelson"/>
    """
    XML_PLAYER_PITCHER_DEBUT = """
    <player id="572140" first="Tyler" last="Skaggs" num="" boxname="Skaggs" rl="L" bats="L" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".hoge" hr="fuga" rbi="bar" wins="_" losses="0" era="-"/>
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
        player = Players.Player(soup.find('player'), 'SEA201508113')
        self.assertEqual(player.retro_game_id, 'SEA201508113')
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

    def test_player_pitcher_row(self):
        """
        Player dataset(pitcher, row)
        """
        soup = BeautifulSoup(TestPlayers.XML_PLAYER_PITCHER, 'lxml')
        player = Players.Player(soup.find('player'), 'SEA201408113')
        row = player.row()
        self.assertEqual(row['retro_game_id'], 'SEA201408113')
        self.assertEqual(row['id'], '547874')
        self.assertEqual(row['first'], 'Hisashi')
        self.assertEqual(row['last'], 'Iwakuma')
        self.assertEqual(row['position'], 'P')
        self.assertEqual(row['num'], 18)
        self.assertEqual(row['box_name'], 'Iwakuma')
        self.assertEqual(row['rl'], 'R')
        self.assertEqual(row['bats'], 'R')
        self.assertEqual(row['status'], 'A')
        self.assertEqual(row['team_abbrev'], 'SEA')
        self.assertEqual(row['team_id'], '136')
        self.assertEqual(row['parent_team_abbrev'], 'SEA')
        self.assertEqual(row['parent_team_id'], '136')
        self.assertEqual(row['bat_order'], 0)
        self.assertEqual(row['game_position'], 'P')
        self.assertEqual(row['avg'], 0.0)
        self.assertEqual(row['hr'], 0)
        self.assertEqual(row['rbi'], 0)
        self.assertEqual(row['wins'], 3)
        self.assertEqual(row['losses'], 2)
        self.assertEqual(row['era'], 4.41)

    def test_player_batter(self):
        """
        Player data(batter)
        """
        soup = BeautifulSoup(TestPlayers.XML_PLAYER_BATTER, 'lxml')
        player = Players.Player(soup.find('player'), 'SEA201508121')
        self.assertEqual(player.retro_game_id, 'SEA201508121')
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

    def test_player_batter_row(self):
        """
        Player dataset(batter, row)
        """
        soup = BeautifulSoup(TestPlayers.XML_PLAYER_BATTER, 'lxml')
        player = Players.Player(soup.find('player'), 'SEA201408121')
        row = player.row()
        self.assertEqual(row['retro_game_id'], 'SEA201408121')
        self.assertEqual(row['id'], '572122')
        self.assertEqual(row['first'], 'Kyle')
        self.assertEqual(row['last'], 'Seager')
        self.assertEqual(row['position'], '3B')
        self.assertEqual(row['num'], 15)
        self.assertEqual(row['box_name'], 'Seager, K')
        self.assertEqual(row['rl'], 'R')
        self.assertEqual(row['bats'], 'L')
        self.assertEqual(row['status'], 'A')
        self.assertEqual(row['team_abbrev'], 'SEA')
        self.assertEqual(row['team_id'], '136')
        self.assertEqual(row['parent_team_abbrev'], 'SEA')
        self.assertEqual(row['parent_team_id'], '136')
        self.assertEqual(row['bat_order'], 2)
        self.assertEqual(row['game_position'], '3B')
        self.assertEqual(row['avg'], 0.263)
        self.assertEqual(row['hr'], 16)
        self.assertEqual(row['rbi'], 45)
        self.assertEqual(row['wins'], 0)
        self.assertEqual(row['losses'], 0)
        self.assertEqual(row['era'], 0.0)

    def test_player_coach(self):
        """
        Coach data
        """
        team = Players.Team()
        team.id = "hoge"
        team.team_type = "away"
        team.name = "name"
        soup = BeautifulSoup(TestPlayers.XML_COACH, 'lxml')
        coach = Players.Coach(soup.find('coach'), 'SEA201508122', team)
        self.assertEqual(coach.retro_game_id, 'SEA201508122')
        self.assertEqual(coach.id, '118576')
        self.assertEqual(coach.first, 'Lloyd')
        self.assertEqual(coach.last, 'McClendon')
        self.assertEqual(coach.position, 'manager')
        self.assertEqual(coach.num, 21)
        self.assertEqual(coach.team_id, "hoge")
        self.assertEqual(coach.team_name, "name")

    def test_player_coach_row(self):
        """
        Coach dataset(row)
        """
        team = Players.Team()
        team.id = "hoge"
        team.team_type = "away"
        team.name = "name"
        soup = BeautifulSoup(TestPlayers.XML_COACH, 'lxml')
        coach = Players.Coach(soup.find('coach'), 'SEA201408122', team)
        row = coach.row()
        self.assertEqual(row['retro_game_id'], 'SEA201408122')
        self.assertEqual(row['id'], '118576')
        self.assertEqual(row['first'], 'Lloyd')
        self.assertEqual(row['last'], 'McClendon')
        self.assertEqual(row['position'], 'manager')
        self.assertEqual(row['num'], 21)
        self.assertEqual(row['team_id'], "hoge")
        self.assertEqual(row['team_name'], "name")

    def test_player_coach_not_number(self):
        """
        Coach data(not exists number)
        """
        team = Players.Team()
        team.id = "fuga"
        team.team_type = "home"
        team.name = "team name"
        soup = BeautifulSoup(TestPlayers.XML_COACH_NOT_NUMBER, 'lxml')
        coach = Players.Coach(soup.find('coach'), 'SEA201508130', team)
        self.assertEqual(coach.retro_game_id, 'SEA201508130')
        self.assertEqual(coach.id, '579474')
        self.assertEqual(coach.first, 'Doug')
        self.assertEqual(coach.last, 'Sisson')
        self.assertEqual(coach.position, 'baserunning/outfield_and_first_base_coach')
        self.assertEqual(coach.num, 'Unknown')
        self.assertEqual(coach.team_id, "fuga")
        self.assertEqual(coach.team_name, "team name")

    def test_player_umpire(self):
        """
        Umpire data
        """
        soup = BeautifulSoup(TestPlayers.XML_UMPIRE, 'lxml')
        umpire = Players.Umpire(soup.find('umpire'), 'SEA201508131')
        self.assertEqual(umpire.retro_game_id, 'SEA201508131')
        self.assertEqual(umpire.id, '427362')
        self.assertEqual(umpire.first, 'Jeff')
        self.assertEqual(umpire.last, 'Nelson')
        self.assertEqual(umpire.position, 'home')
        self.assertEqual(umpire.name, 'Jeff Nelson')

    def test_player_umpire_row(self):
        """
        Umpire dataset(row)
        """
        soup = BeautifulSoup(TestPlayers.XML_UMPIRE, 'lxml')
        umpire = Players.Umpire(soup.find('umpire'), 'SEA201408131')
        row = umpire.row()
        self.assertEqual(row['retro_game_id'], 'SEA201408131')
        self.assertEqual(row['id'], '427362')
        self.assertEqual(row['first'], 'Jeff')
        self.assertEqual(row['last'], 'Nelson')
        self.assertEqual(row['position'], 'home')
        self.assertEqual(row['name'], 'Jeff Nelson')

    def test_player_pitcher_debut(self):
        """
        Player data(pitcher, debut)
        """
        soup = BeautifulSoup(TestPlayers.XML_PLAYER_PITCHER_DEBUT, 'lxml')
        player = Players.Player(soup.find('player'), 'SEA201508140')
        self.assertEqual(player.retro_game_id, 'SEA201508140')
        self.assertEqual(player.id, '572140')
        self.assertEqual(player.first, 'Tyler')
        self.assertEqual(player.last, 'Skaggs')
        self.assertEqual(player.position, 'P')
        self.assertEqual(player.num, 'Unknown')
        self.assertEqual(player.box_name, 'Skaggs')
        self.assertEqual(player.rl, 'L')
        self.assertEqual(player.bats, 'L')
        self.assertEqual(player.status, 'A')
        self.assertEqual(player.team_abbrev, 'LAA')
        self.assertEqual(player.team_id, '108')
        self.assertEqual(player.parent_team_abbrev, 'LAA')
        self.assertEqual(player.parent_team_id, '108')
        self.assertEqual(player.bat_order, 'U')
        self.assertEqual(player.game_position, 'U')
        self.assertEqual(player.avg, 0.0)
        self.assertEqual(player.hr, 0)
        self.assertEqual(player.rbi, 0)
        self.assertEqual(player.wins, 0)
        self.assertEqual(player.losses, 0)
        self.assertEqual(player.era, 0.0)

if __name__ == '__main__':
    main()

