#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
from pitchpx.mlbam_util import MlbamUtil

__author__ = 'Shinichi Nakagawa'


class Inning(object):

    DIRECTORY = 'inning'
    FILENAME_PATTERN = 'inning_\d*.xml'
    TAG = 'a'
    INNING_TOP = 'top'
    INNING_BOTTOM = 'bottom'
    INNINGS = (INNING_TOP, INNING_BOTTOM)
    atbats = {}
    pitches = {}

    def __init__(self, game, players):
        """
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        """
        self.game = game
        self.players = players

    @classmethod
    def read_xml(cls, url, markup, game, players):
        """
        read xml object
        :param url: contents url
        :param markup: markup provider
        :param game: MLBAM Game object
        :param players: MLBAM Players object
        :return: pitchpx.game.game.Game object
        """
        innings = Inning(game, players)
        base_url = "".join([url, cls.DIRECTORY])
        for inning in MlbamUtil.find_xml_all(base_url, markup, cls.TAG, cls.FILENAME_PATTERN):
            soup = MlbamUtil.find_xml("/".join([base_url, inning.get_text().strip()]), markup)
            inning_number = int(soup.inning['num'])
            for inning in cls.INNINGS:
                inning_soup = soup.inning.find(inning)
                innings._inning_events(inning_soup, inning_number)
        return innings

    def _inning_events(self, soup, inning_number):
        """
        Inning Events.
        :param soup: Beautifulsoup object
        :param inning_number: Inning Number
        """
        # at bat(batter box data)
        for ab in soup.find_all('atbat'):
            self.atbats.update(self._get_atbat(ab))

        # pitching data
        for pitch in soup.find_all('pitch'):
            self.pitches.update(self._get_pitch(pitch))

    def _get_atbat(self, soup):
        """
        get atbat data
        :param soup: Beautifulsoup object
        :return: atbat result
        """
        atbats = {}
        # TODO append at bat event
        print(soup)
        return atbats

    def _get_pitch(self, soup):
        """
        get pitch data
        :param soup: Beautifulsoup object
        :return: pitches result
        """
        pitch = {}
        # TODO append pitch event
        print(soup)
        return pitch
