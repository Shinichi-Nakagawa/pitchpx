#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        Baseball people(Japanese "やきう民")
        """
        id = MlbamConst.UNKNOWN_FULL
        first = MlbamConst.UNKNOWN_FULL
        last = MlbamConst.UNKNOWN_FULL
        position = MlbamConst.UNKNOWN_SHORT

        def __init__(self, soup):
            """
            create object
            :param soup: Beautifulsoup object
            """
            self.id = soup['id']
            self.first = soup['first']
            self.last = soup['last']
            self.position = soup['position']

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

        def __init__(self, soup):
            """
            create object
            :param soup: Beautifulsoup object
            """
            super().__init__(soup)
            self.num = int(soup['num'])
            self.box_name = soup['boxname']
            self.rl = soup['rl']
            self.bats = soup['bats']
            self.status = soup['status']
            self.team_abbrev = soup['team_abbrev']
            self.team_id = soup['team_id']
            self.parent_team_abbrev = soup['parent_team_abbrev']
            self.parent_team_id = soup['parent_team_id']
            if 'avg' in soup.attrs:
                self.avg = float(soup['avg'])
            if 'hr' in soup.attrs:
                self.hr = int(soup['hr'])
            if 'rbi' in soup.attrs:
                self.rbi = int(soup['rbi'])
            if 'wins' in soup.attrs:
                self.wins = int(soup['wins'])
            if 'losses' in soup.attrs:
                self.losses = int(soup['losses'])
            if 'era' in soup.attrs:
                self.era = float(soup['era'])
            if 'bat_order' in soup.attrs:
                self.bat_order = int(soup['bat_order'])
            if 'game_position' in soup.attrs:
                self.game_position = soup['game_position']

    class Coach(YakyuMin):
        """
        Coach Data
        """
        num = MlbamConst.UNKNOWN_FULL
        team_id = MlbamConst.UNKNOWN_SHORT
        team_name = MlbamConst.UNKNOWN_FULL

        def __init__(self, soup, team):
            """
            create object
            :param soup: Beautifulsoup object
            :param team: Team object
            """
            super().__init__(soup)
            self.num = int(soup['num'])
            self.team_id = team.id
            self.team_name = team.name

    class Umpire(YakyuMin):
        """
        Umpire Data
        """
        name = MlbamConst.UNKNOWN_FULL

        def __init__(self, soup):
            """
            create object
            :param soup: Beautifulsoup object
            """
            super().__init__(soup)
            self.name = soup['name']

    def __init__(self):
        self.game = self.Game()

    @classmethod
    def read_xml(cls, url, markup):
        """
        read xml object
        :param url: contents url
        :param markup: markup provider
        :return: pitchpx.game.players.Players object
        """
        players = Players()
        players.game = Players.Game()

        soup = MlbamUtil.find_xml("/".join([url, cls.FILENAME]), markup)
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
            players.rosters.update({player['id']: cls.Player(player) for player in team.find_all('player')})
            # coach data
            players.coaches.update({coach['id']: cls.Coach(coach, team_object) for coach in team.find_all('coach')})
        # umpire data
        umpires = soup.find('umpires')
        players.umpires.update({umpire['id']: cls.Umpire(umpire) for umpire in umpires.find_all('umpire')})
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
