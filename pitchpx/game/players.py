#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from pitchpx.mlbam_util import MlbamUtil, MlbamConst
from pitchpx.game.game import Game

__author__ = 'Shinichi Nakagawa'


class Players(object):

    FILENAME = 'players.xml'
    rosters = {}  # key: player id value: Player object
    umpires = {}  # key: umpire id value: Umpire object
    coaches = {}  # key: coache id value: Coache object
    home_team = None
    away_team = None
    game = None

    class YakyuMin(object):
        """
        Baseball Human Base Class
        """
        retro_game_id = MlbamConst.UNKNOWN_FULL
        id = MlbamConst.UNKNOWN_FULL
        first = MlbamConst.UNKNOWN_FULL
        last = MlbamConst.UNKNOWN_FULL
        position = MlbamConst.UNKNOWN_SHORT

        def __init__(self, soup, retro_game_id):
            """
            create object
            :param soup: Beautifulsoup object
            :param retro_game_id: Retrosheet Game id
            """
            self.retro_game_id = retro_game_id
            self.id = soup.get('id')
            self.first = soup.get('first')
            self.last = soup.get('last')
            self.position = soup.get('position')

        def row(self):
            """
            Yakyu-Min Dataset(Row)
            :return: {
                'retro_game_id': Retrosheet Game id
                'id': Player or Coach or Umpire Id
                'first': First Name
                'last': Last Name
                'position': Position
            }
            """
            row = OrderedDict()
            row['retro_game_id'] = self.retro_game_id
            row['id'] = self.id
            row['first'] = self.first
            row['last'] = self.last
            row['position'] = self.position
            return row

    class Team(object):
        """
        Team Data
        """
        id = MlbamConst.UNKNOWN_SHORT
        team_type = MlbamConst.UNKNOWN_SHORT
        name = MlbamConst.UNKNOWN_FULL

    class Game(object):
        """
        Game Data(summary)
        """
        venue = MlbamConst.UNKNOWN_FULL
        date = MlbamConst.UNKNOWN_FULL

    class Player(YakyuMin):
        """
        Player's Data(Pitcher/Batter)
        """
        num = MlbamConst.UNKNOWN_FULL
        box_name = MlbamConst.UNKNOWN_FULL
        rl = MlbamConst.UNKNOWN_SHORT
        bats = MlbamConst.UNKNOWN_SHORT
        status = MlbamConst.UNKNOWN_FULL
        team_abbrev = MlbamConst.UNKNOWN_FULL
        team_id = MlbamConst.UNKNOWN_FULL
        parent_team_abbrev = MlbamConst.UNKNOWN_FULL
        parent_team_id = MlbamConst.UNKNOWN_FULL
        avg = 0.0
        hr = 0
        rbi = 0
        wins = 0
        losses = 0
        era = 0.0
        bat_order = MlbamConst.UNKNOWN_SHORT
        game_position = MlbamConst.UNKNOWN_SHORT

        DOWNLOAD_FILE_NAME = 'mlbam_player_{day}.{extension}'

        def __init__(self, soup, retro_game_id):
            """
            create object
            :param soup: Beautifulsoup object
            :param retro_game_id: Retrosheet Game id
            """
            super().__init__(soup, retro_game_id)
            if Players.isdigit(soup['num']):
                self.num = int(soup['num'])
            self.box_name = soup['boxname']
            self.rl = soup.get('rl')
            self.bats = soup.get('bats')
            self.status = soup.get('status')
            self.team_abbrev = soup.get('team_abbrev')
            self.team_id = soup.get('team_id')
            self.parent_team_abbrev = soup.get('parent_team_abbrev')
            self.parent_team_id = soup.get('parent_team_id')
            if 'avg' in soup.attrs and Players.isdigit(soup['avg']):
                self.avg = float(soup['avg'])
            if 'hr' in soup.attrs and Players.isdigit(soup['hr']):
                self.hr = int(soup['hr'])
            if 'rbi' in soup.attrs and Players.isdigit(soup['rbi']):
                self.rbi = int(soup['rbi'])
            if 'wins' in soup.attrs and Players.isdigit(soup['wins']):
                self.wins = int(soup['wins'])
            if 'losses' in soup.attrs and Players.isdigit(soup['losses']):
                self.losses = int(soup['losses'])
            if 'era' in soup.attrs and Players.isdigit(soup['era']):
                self.era = float(soup['era'])
            if 'bat_order' in soup.attrs and Players.isdigit(soup['bat_order']):
                self.bat_order = int(soup['bat_order'])
            if 'game_position' in soup.attrs:
                self.game_position = soup['game_position']

        def row(self):
            """
            Player's Dataset(Row)
            :return: {
                'retro_game_id': Retrosheet Game id
                'id': Player or Coach or Umpire Id
                'first': First Name
                'last': Last Name
                'position': Position
                'num': Unique Number in Game
                'box_name': At Bat Name
                'rl': Throw(R or L)
                'bats': Batting Position(R or L or S)
                'status': A(Active) or Other
                'team_abbrev': Team Name
                'team_id': Team Id
                'parent_team_abbrev': Base Team Name
                'parent_team_id': Base Team Id
                'avg': Batting Average
                'hr': Home Run
                'rbi': RBI
                'wins': Pitched Win
                'lose': Pithced Lose
                'era': ERA
                'bat_order': Batting Order num(Starting Member Only)
                'game_position': Game Position(Starting Member Only)
            }
            """
            row = super().row()
            row['num'] = self.num
            row['box_name'] = self.box_name
            row['rl'] = self.rl
            row['bats'] = self.bats
            row['status'] = self.status
            row['team_abbrev'] = self.team_abbrev
            row['team_id'] = self.team_id
            row['parent_team_abbrev'] = self.parent_team_abbrev
            row['parent_team_id'] = self.parent_team_id
            row['avg'] = self.avg
            row['hr'] = self.hr
            row['rbi'] = self.rbi
            row['wins'] = self.wins
            row['losses'] = self.losses
            row['era'] = self.era
            row['bat_order'] = self.bat_order
            row['game_position'] = self.game_position
            return row

    class Coach(YakyuMin):
        """
        Coach Data
        """
        num = MlbamConst.UNKNOWN_FULL
        team_id = MlbamConst.UNKNOWN_SHORT
        team_name = MlbamConst.UNKNOWN_FULL

        DOWNLOAD_FILE_NAME = 'mlbam_coach_{day}.{extension}'

        def __init__(self, soup, retro_game_id, team):
            """
            create object
            :param soup: Beautifulsoup object
            :param retro_game_id: Retrosheet Game id
            :param team: Team object
            """
            super().__init__(soup, retro_game_id)
            if Players.isdigit(soup['num']):
                self.num = int(soup['num'])
            self.team_id = team.id
            self.team_name = team.name

        def row(self):
            """
            Coach Dataset(Row)
            :return: {
                'retro_game_id': Retrosheet Game id
                'id': Player or Coach or Umpire Id
                'first': First Name
                'last': Last Name
                'position': Position
                'num': Unique Number in Game
                'team_id': Team Id
                'team_name': Team Name
            }
            """
            row = super().row()
            row['num'] = self.num
            row['team_id'] = self.team_id
            row['team_name'] = self.team_name
            return row

    class Umpire(YakyuMin):
        """
        Umpire Data
        """
        name = MlbamConst.UNKNOWN_FULL

        DOWNLOAD_FILE_NAME = 'mlbam_umpire_{day}.{extension}'

        def __init__(self, soup, retro_game_id):
            """
            create object
            :param soup: Beautifulsoup object
            :param retro_game_id: Retrosheet Game id
            """
            super().__init__(soup, retro_game_id)
            self.name = soup['name']

        def row(self):
            """
            Umpire Dataset(Row)
            :return: {
                'retro_game_id': Retrosheet Game id
                'id': Player or Coach or Umpire Id
                'first': First Name
                'last': Last Name
                'position': Position
                'name': At Bat Name
            }
            """
            row = super().row()
            row['name'] = self.name
            return row

    def __init__(self):
        self.game = self.Game()
        self.rosters, self.coaches, self.umpires = {}, {}, {}

    @classmethod
    def read_xml(cls, url, markup, game):
        """
        read xml object
        :param url: contents url
        :param markup: markup provider
        :param game: MLBAM Game object
        :return: pitchpx.game.players.Players object
        """
        return Players._read_objects(MlbamUtil.find_xml("".join([url, cls.FILENAME]), markup) ,game)

    @classmethod
    def _read_objects(cls, soup, game):
        """
        read objects
        :param soup: Beautifulsoup object
        :param game: MLBAM Game object
        :return: pitchpx.game.players.Players object
        """
        players = Players()
        players.game = Players.Game()
        # game data
        players.game.venue = soup.game['venue']
        players.game.date = soup.game['date']
        # players & team data
        for team in soup.find_all('team'):
            team_object = cls._get_team(team)
            if team['type'] == Game.TEAM_TYPE_HOME:
                # team data(home)
                players.home_team = team_object
            elif team['type'] == Game.TEAM_TYPE_AWAY:
                # team data(away)
                players.away_team = team_object
            # player data
            players.rosters.update(
                    {player['id']: cls.Player(player, game.retro_game_id) for player in team.find_all('player')}
            )
            # coach data
            players.coaches.update(
                    {coach['id']: cls.Coach(coach, game.retro_game_id, team_object) for coach in team.find_all('coach')}
            )
        # umpire data
        umpires = soup.find('umpires')
        players.umpires.update(
                {umpire['id']: cls.Umpire(umpire, game.retro_game_id) for umpire in umpires.find_all('umpire')}
        )
        return players

    @classmethod
    def _get_team(cls, soup):
        """
        get team data
        :param soup: Beautifulsoup object
        :return: pitchpx.game.players.Players.Team object
        """
        team = cls.Team()
        team.team_type = soup['type']
        team.id = soup['id']
        team.name = soup['name']
        return team

    @classmethod
    def isdigit(cls, value):
        """
        ditit check for stats
        :param value: stats value
        :return: True or False
        """
        if str(value).replace('.','').replace('-','').isdigit():
            return True
        return False
