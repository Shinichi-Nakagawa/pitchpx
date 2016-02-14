#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'


class RetroSheet(object):

    EVENT_02_GENERIC_OUT_FLYBALL = ('flyout', 'fly out', 'sac fly', 'sac fly dp')
    EVENT_02_GENERIC_OUT_LINEDRIVE = ('lineout', 'line out', 'bunt lineout')
    EVENT_02_GENERIC_OUT_POPUP = ('pop out', 'bunt pop out')
    EVENT_02_GENERIC_OUT_GROUNDBALL = ('groundout', 'ground out', 'sac bunt', 'bunt groundout', 'grounded into dp')
    EVENT_02_GENERIC_OUT_OTHER = ('forceout', 'double play', 'triple play', 'sacrifice bunt d')
    EVENT_03_STRIKE_OUT = ('strikeout', 'strikeout - dp')
    EVENT_14_WALK = ('walk', )
    EVENT_15_INTENT_WALK = ('intent walk', )
    EVENT_16_HIT_BY_PITCH = ('hit by pitch', )
    EVENT_19_FIELDERS_CHOICE = ('fielders choice out', 'fielders choice')
    EVENT_20_SINGLE = ('single', )
    EVENT_21_DOUBLE = ('double', )
    EVENT_22_TRIPLE = ('triple', )
    EVENT_23_HOME_RUN = ('home run', )
    EVENT_CD_HITS = (20, 21, 22, 23)

    @classmethod
    def event_cd(cls, event_tx, ab_des):
        """
        Event Code for Retrosheet
        :param event_tx: Event text
        :param ab_des: at bat description
        :return: event_cd(int)
        """
        _event_tx = event_tx.lower()
        _ab_des = ab_des.lower()
        # Generic out(event_cd:2)
        if _event_tx in cls.EVENT_02_GENERIC_OUT_FLYBALL:
            return 2
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_LINEDRIVE:
            return 2
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_POPUP:
            return 2
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_GROUNDBALL:
            return 2
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_OTHER:
            return 2
        # Strike out(event_cd:3)
        elif _event_tx in cls.EVENT_03_STRIKE_OUT:
            return 3
        # Walk(event_cd:14)
        elif _event_tx in cls.EVENT_14_WALK:
            return 14
        # Intent Walk(event_cd:15)
        elif _event_tx in cls.EVENT_15_INTENT_WALK:
            return 15
        # Hit By Pitch(event_cd:16)
        elif _event_tx in cls.EVENT_16_HIT_BY_PITCH:
            return 16
        # Interference(event_cd:17)
        elif _event_tx.lower().count('interference') > 0:
            return 17
        # Error(event_cd:18)
        elif _event_tx[-5:] == 'error':
            return 18
        # Fielder's choice(event_cd:19)
        elif _event_tx in cls.EVENT_19_FIELDERS_CHOICE:
            return 19
        # Single(event_cd:20)
        elif _event_tx in cls.EVENT_20_SINGLE:
            return 20
        # 2B(event_cd:21)
        elif _event_tx in cls.EVENT_21_DOUBLE:
            return 21
        # 3B(event_cd:22)
        elif _event_tx in cls.EVENT_22_TRIPLE:
            return 22
        # HR(event_cd:22)
        elif _event_tx in cls.EVENT_23_HOME_RUN:
            return 23
        # Runner Out
        elif _event_tx == 'runner out':
            # Caught stealing(event_cd:6)
            if _ab_des.count("caught stealing") > 0:
                return 6
            # Picks off(event_cd:6)
            elif _ab_des.count("picks off") > 0:
                return 8
            # Unknown event(event_cd:0)
            else:
                return 0
        # Unknown event(event_cd:0)
        else:
            return 0

    @classmethod
    def battedball_cd(cls, event_cd, event_tx, ab_des):
        """
        Batted ball Code for Retrosheet
        :param event_cd: Event code
        :param event_tx: Event text
        :param ab_des: at bat description
        :return: battedball_cd(str)
        """
        _event_tx = event_tx.lower()
        # Fly Out
        if _event_tx in cls.EVENT_02_GENERIC_OUT_FLYBALL:
            return 'F'
        # Line Out
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_LINEDRIVE:
            return 'L'
        # Pop Out
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_POPUP:
            return 'P'
        # Grounder
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_GROUNDBALL:
            return 'G'
        # Force out, double play, triple play
        elif _event_tx in cls.EVENT_02_GENERIC_OUT_OTHER:
            return cls._battedball_cd(ab_des)
        # Single, 2B, 3B, HR
        elif event_cd in cls.EVENT_CD_HITS:
            return cls._battedball_cd(ab_des)
        # Unknown
        else:
            return ''

    @classmethod
    def _battedball_cd(cls, ab_des):
        """
        Batted ball Code for at bat description
        :param ab_des: at bat description
        :return: battedball_cd(str)
        """
        _ab_des = ab_des.lower()
        if ab_des.count("ground")>0:
            return 'G'
        elif _ab_des.count("lines")>0:
            return 'L'
        elif _ab_des.count("flies")>0:
            return 'F'
        elif _ab_des.count("pops")>0:
            return 'P'
        elif _ab_des.count("on a line drive")>0:
            return 'L'
        elif _ab_des.count("fly ball")>0:
            return 'F'
        elif _ab_des.count("ground ball")>0:
            return 'G'
        elif _ab_des.count("pop up")>0:
            return 'P'
        else:
            return ''

    @classmethod
    def ball_count(cls, ball_tally, strike_tally, pitch_res):
        """
        Ball/Strike counter
        :param ball_tally: Ball telly
        :param strike_tally: Strike telly
        :param pitch_res: pitching result(Retrosheet format)
        :return: ball count, strike count
        """
        b, s = ball_tally, strike_tally
        if pitch_res == "B":
            if ball_tally < 4:
                b += 1
        elif pitch_res == "S" or pitch_res == "C" or pitch_res == "X":
            if strike_tally < 3:
                s += 1
        elif pitch_res == "F":
            if strike_tally < 2:
                s += 1
        return b, s

    @classmethod
    def is_pa_terminal(cls, ball_tally, strike_tally, pitch_res, event_cd):
        """
        Is PA terminal
        :param ball_tally: Ball telly
        :param strike_tally: Strike telly
        :param pitch_res: pitching result(Retrosheet format)
        :param event_cd: Event code
        :return: True or False
        """
        # In Play
        if pitch_res == 'X':
            return True
        # Strike Out(Strike or Call)
        elif (pitch_res == 'S' or pitch_res == 'C') and event_cd == 3 and strike_tally == 2:
            return True
        # Walk(Ball or Intent Ball)
        elif pitch_res == 'B' and (event_cd == 14 or event_cd == 15) and ball_tally == 3:
            return True
        return False
