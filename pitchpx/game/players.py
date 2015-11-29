#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pitchpx.mlbam_util import MlbamUtil

__author__ = 'Shinichi Nakagawa'


class Players(object):
    FILENAME = 'players.xml'

    @classmethod
    def read_xml(cls, url, markup):
        """
        read xml object
        :param url: contents url
        :param markup: markup provider
        :return: pitchpx.game.players.Players object
        """
        players = Players()
        soup = MlbamUtil.find_xml("/".join([url, cls.FILENAME]), markup)
        # TODO content生成
        return players
