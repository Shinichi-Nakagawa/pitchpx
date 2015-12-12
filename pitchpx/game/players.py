#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pitchpx.mlbam_util import MlbamUtil, MlbamConst
from pitchpx.game.game import Game

__author__ = 'Shinichi Nakagawa'


class Player(object):
    """
    Player's Data(Pitcher/Batter)
    """

    id = MlbamConst.UNKNOWN_FULL
    first = MlbamConst.UNKNOWN_FULL
    last = MlbamConst.UNKNOWN_FULL
    num = MlbamConst.UNKNOWN_FULL
    box_name = MlbamConst.UNKNOWN_FULL
    rl = MlbamConst.UNKNOWN_SHORT
    bats = MlbamConst.UNKNOWN_SHORT
    position = MlbamConst.UNKNOWN_SHORT
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

    def __init__(self, soup):
        """
        create object
        :param soup: Beautifulsoup object
        """
        self.id = soup['id']
        self.first = soup['first']
        self.last = soup['last']
        self.num = int(soup['num'])
        self.box_name = soup['boxname']
        self.rl = soup['rl']
        self.bats = soup['bats']
        self.position = soup['position']
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


class Coach(object):
    """
    Coach Data
    """
    pass


class Umpire(object):
    """
    Umpire Data
    """
    pass


class Players(object):

    FILENAME = 'players.xml'
    rosters = {}
    umpires = {}
    coaches = {}
    home_team = None
    away_team = None
    game = None

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
            if team['type'] == Game.TEAM_TYPE_HOME:
                # team data(home)
                players.home_team = cls._get_team(team)
            elif team['type'] == Game.TEAM_TYPE_AWAY:
                # team data(away)
                players.away_team = cls._get_team(team)
            # player data
            players.rosters.update(cls._get_players(team))
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
    def _get_players(cls, soup):
        """
        get player list
        :param soup: Beautifulsoup object
        :return: pitchpx.game.players.Player list
        """
        players = {}
        for player in (soup.find_all('player')):
            players[player['id']] = Player(player)
        return players


# TODO デバッグ用、後で消す
if __name__ == '__main__':
    players = Players.read_xml('http://gd2.mlb.com/components/game/mlb/year_2015/month_08/day_12/gid_2015_08_12_balmlb_seamlb_1', 'lxml')
    print(players.players)
    print(players.umpires)
    print(players.coaches)