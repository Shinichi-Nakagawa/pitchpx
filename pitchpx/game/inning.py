#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pitchpx.mlbam_util import MlbamUtil

__author__ = 'Shinichi Nakagawa'


class Inning(object):
    DIRECTORY = 'inning'
    FILENAME_PATTERN = 'inning_\d*.xml'
    TAG = 'a'

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
        innings = []
        base_url = "/".join([url, cls.DIRECTORY])
        for inning in MlbamUtil.find_xml_all(base_url, markup, cls.TAG, cls.FILENAME_PATTERN):
            soup = MlbamUtil.find_xml("".join([base_url, inning.get_text().strip()]), markup)
            print(soup)
        return innings
