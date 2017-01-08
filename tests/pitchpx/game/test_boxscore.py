#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from datetime import datetime as dt
from bs4 import BeautifulSoup
from unittest import TestCase, main
from pitchpx.game.boxscore import BoxScore
from pitchpx.game.game import Game
from pitchpx.game.players import Players

__author__ = 'Shinichi Nakagawa'


class TestBoxScore(TestCase):

    XML_BOXSCORE = """
<?xml version="1.0" encoding="UTF-8"?><!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt-->
<boxscore game_id="2013/04/29/anamlb-oakmlb-1" game_pk="347121" venue_id="10"
          venue_name="O.co Coliseum"
          home_sport_code="mlb"
          away_team_code="ana"
          home_team_code="oak"
          away_id="108"
          home_id="133"
          away_fname="Los Angeles Angels"
          home_fname="Oakland Athletics"
          away_sname="LA Angels"
          home_sname="Oakland"
          date="April 29, 2013"
          away_wins="9"
          away_loss="16"
          home_wins="15"
          home_loss="12"
          status_ind="F">
   <linescore away_team_runs="8" home_team_runs="10" away_team_hits="15" home_team_hits="15"
              away_team_errors="3"
              home_team_errors="1"
              note="Two out when winning run scored.">
      <inning_line_score away="1" home="0" inning="1"/>
      <inning_line_score away="1" home="0" inning="2"/>
      <inning_line_score away="0" home="0" inning="3"/>
      <inning_line_score away="0" home="1" inning="4"/>
      <inning_line_score away="4" home="0" inning="5"/>
      <inning_line_score away="0" home="1" inning="6"/>
      <inning_line_score away="1" home="0" inning="7"/>
      <inning_line_score away="0" home="4" inning="8"/>
      <inning_line_score away="0" home="1" inning="9"/>
      <inning_line_score away="0" home="0" inning="10"/>
      <inning_line_score away="0" home="0" inning="11"/>
      <inning_line_score away="0" home="0" inning="12"/>
      <inning_line_score away="0" home="0" inning="13"/>
      <inning_line_score away="0" home="0" inning="14"/>
      <inning_line_score away="1" home="1" inning="15"/>
      <inning_line_score away="0" home="0" inning="16"/>
      <inning_line_score away="0" home="0" inning="17"/>
      <inning_line_score away="0" home="0" inning="18"/>
      <inning_line_score away="0" home="2" inning="19"/>
   </linescore>
   <pitching team_flag="away" out="56" h="15" r="10" er="8" bb="6" so="17" hr="2" bf="77"
             era="4.65">
      <pitcher id="462102" name="Hanson" name_display_first_last="Tommy Hanson" pos="P"
               out="18"
               bf="24"
               er="1"
               r="2"
               h="4"
               so="6"
               hr="1"
               bb="1"
               np="100"
               s="65"
               w="2"
               l="1"
               sv="0"
               bs="0"
               hld="0"
               s_ip="23.0"
               s_h="24"
               s_r="10"
               s_er="9"
               s_bb="7"
               s_so="14"
               game_score="63"
               era="3.52"/>
      <pitcher id="607706" name="Roth" name_display_first_last="Michael Roth" pos="P" out="3"
               bf="6"
               er="3"
               r="3"
               h="3"
               so="0"
               hr="0"
               bb="0"
               np="23"
               s="13"
               w="1"
               l="1"
               sv="0"
               bs="0"
               hld="0"
               s_ip="9.2"
               s_h="14"
               s_r="10"
               s_er="10"
               s_bb="3"
               s_so="10"
               game_score="35"
               era="9.31"/>
      <pitcher id="451773" name="De La Rosa, D" name_display_first_last="Dane De La Rosa"
               pos="P"
               out="2"
               bf="4"
               er="1"
               r="1"
               h="1"
               so="1"
               hr="0"
               bb="1"
               np="11"
               s="5"
               w="1"
               l="0"
               sv="0"
               bs="0"
               hld="3"
               s_ip="12.1"
               s_h="11"
               s_r="4"
               s_er="4"
               s_bb="5"
               s_so="12"
               game_score="46"
               era="2.92"
               note="(H, 3)"/>
      <pitcher id="275933" name="Downs, S" name_display_first_last="Scott Downs" pos="P"
               out="0"
               bf="1"
               er="0"
               r="0"
               h="1"
               so="0"
               hr="0"
               bb="0"
               np="4"
               s="2"
               w="0"
               l="2"
               sv="0"
               bs="2"
               hld="4"
               s_ip="10.2"
               s_h="10"
               s_r="4"
               s_er="3"
               s_bb="5"
               s_so="8"
               game_score="48"
               era="2.53"/>
      <pitcher id="457117" name="Frieri" name_display_first_last="Ernesto Frieri" pos="P"
               out="4"
               bf="6"
               er="1"
               r="1"
               h="1"
               so="2"
               hr="0"
               bb="1"
               np="27"
               s="17"
               w="0"
               l="1"
               sv="3"
               bs="1"
               hld="0"
               s_ip="10.2"
               s_h="7"
               s_r="3"
               s_er="3"
               s_bb="8"
               s_so="14"
               game_score="49"
               era="2.53"
               blown_save="true"
               note="(BS, 1)">(BS, 1)</pitcher>
      <pitcher id="425532" name="Williams" name_display_first_last="Jerome Williams" pos="P"
               out="18"
               bf="23"
               er="0"
               r="1"
               h="4"
               so="2"
               hr="0"
               bb="2"
               np="73"
               s="45"
               w="1"
               l="0"
               sv="0"
               bs="0"
               hld="0"
               s_ip="21.1"
               s_h="16"
               s_r="7"
               s_er="4"
               s_bb="6"
               s_so="11"
               game_score="62"
               era="1.69"/>
      <pitcher id="543409" name="Kohn" name_display_first_last="Michael Kohn" pos="P" out="6"
               bf="6"
               er="0"
               r="0"
               h="0"
               so="4"
               hr="0"
               bb="0"
               np="31"
               s="20"
               w="0"
               l="0"
               sv="0"
               bs="0"
               hld="0"
               s_ip="4.0"
               s_h="3"
               s_r="2"
               s_er="2"
               s_bb="0"
               s_so="6"
               game_score="60"
               era="4.50"/>
      <pitcher id="446264" name="Enright" name_display_first_last="Barry Enright" pos="P"
               out="5"
               bf="7"
               er="2"
               r="2"
               h="1"
               so="2"
               hr="1"
               bb="1"
               np="28"
               s="18"
               w="0"
               l="1"
               sv="0"
               bs="0"
               hld="0"
               s_ip="1.2"
               s_h="1"
               s_r="2"
               s_er="2"
               s_bb="1"
               s_so="2"
               game_score="46"
               era="10.80"
               loss="true"
               note="(L, 0-1)"/>
   </pitching>
   <batting team_flag="home" ab="71" r="10" h="15" d="1" t="1" hr="2" rbi="9" bb="6"
            po="57"
            da="19"
            so="17"
            lob="30"
            avg=".251">
      <batter id="424825" name="Crisp" name_display_first_last="Coco Crisp" pos="CF" bo="100"
              ab="6"
              po="2"
              r="2"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="0"
              lob="0"
              fldg="1.000"
              sb="1"
              cs="0"
              s_hr="5"
              s_rbi="12"
              s_h="28"
              s_bb="17"
              s_r="24"
              s_so="7"
              avg=".283"
              go="3"
              ao="1"/>
      <batter id="474384" name="Freiman" name_display_first_last="Nate Freiman" pos="1B"
              bo="101"
              ab="2"
              po="6"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="1"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="1"
              s_rbi="5"
              s_h="4"
              s_bb="4"
              s_r="2"
              s_so="5"
              avg=".148"
              ao="2"/>
      <batter id="452234" name="Smith, S" name_display_first_last="Seth Smith" pos="DH-LF"
              bo="200"
              ab="8"
              po="0"
              r="0"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="2"
              e="0"
              d="0"
              hbp="0"
              so="2"
              hr="0"
              rbi="0"
              lob="1"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="3"
              s_rbi="13"
              s_h="24"
              s_bb="10"
              s_r="12"
              s_so="18"
              avg=".312"
              go="1"
              ao="3"/>
      <batter id="476704" name="Lowrie" name_display_first_last="Jed Lowrie" pos="SS"
              bo="300"
              ab="9"
              po="2"
              r="2"
              a="6"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="2"
              e="1"
              d="1"
              hbp="0"
              so="1"
              hr="0"
              rbi="1"
              lob="3"
              fldg=".889"
              sb="0"
              cs="0"
              s_hr="3"
              s_rbi="15"
              s_h="34"
              s_bb="13"
              s_r="18"
              s_so="19"
              avg=".333"
              go="3"
              ao="3"/>
      <batter id="493316" name="Cespedes" name_display_first_last="Yoenis Cespedes"
              pos="LF-CF"
              bo="400"
              ab="8"
              po="6"
              r="1"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="4"
              hr="0"
              rbi="1"
              lob="3"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="4"
              s_rbi="10"
              s_h="11"
              s_bb="7"
              s_r="10"
              s_so="19"
              avg=".208"
              go="1"
              ao="2"/>
      <batter id="461235" name="Moss" name_display_first_last="Brandon Moss" pos="1B-RF"
              bo="500"
              ab="8"
              po="10"
              r="3"
              a="2"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="3"
              e="0"
              d="0"
              hbp="0"
              so="4"
              hr="2"
              rbi="3"
              lob="4"
              fldg="1.000"
              sb="1"
              cs="0"
              s_hr="4"
              s_rbi="19"
              s_h="25"
              s_bb="13"
              s_r="17"
              s_so="28"
              avg=".298"
              go="1"
              ao="0"/>
      <batter id="518626" name="Donaldson" name_display_first_last="Josh Donaldson" pos="3B"
              bo="600"
              ab="7"
              po="2"
              r="1"
              a="3"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="3"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="2"
              lob="0"
              fldg="1.000"
              sb="1"
              cs="0"
              s_hr="2"
              s_rbi="20"
              s_h="32"
              s_bb="13"
              s_r="14"
              s_so="13"
              avg=".327"
              go="1"
              ao="2"/>
      <batter id="444379" name="Jaso" name_display_first_last="John Jaso" pos="C" bo="700"
              ab="2"
              po="7"
              r="0"
              a="1"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="0"
              lob="2"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="1"
              s_rbi="9"
              s_h="20"
              s_bb="6"
              s_r="8"
              s_so="16"
              avg=".260"
              go="1"
              ao="0"/>
      <batter id="519083" name="Norris, D" name_display_first_last="Derek Norris" pos="PH-C"
              bo="701"
              ab="5"
              po="11"
              r="1"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="0"
              lob="4"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="4"
              s_h="11"
              s_bb="11"
              s_r="11"
              s_so="11"
              avg=".256"
              note="a-"
              go="2"
              ao="2"/>
      <batter id="502210" name="Reddick" name_display_first_last="Josh Reddick" pos="RF"
              bo="800"
              ab="3"
              po="4"
              r="0"
              a="1"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="3"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="1"
              s_rbi="13"
              s_h="11"
              s_bb="9"
              s_r="9"
              s_so="21"
              avg=".147"
              go="2"
              ao="1"/>
      <batter id="455759" name="Young, C" name_display_first_last="Chris Young"
              pos="PH-RF-CF"
              bo="801"
              ab="4"
              po="2"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="1"
              sf="0"
              h="2"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="1"
              lob="4"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="4"
              s_rbi="15"
              s_h="15"
              s_bb="12"
              s_r="12"
              s_so="20"
              avg=".172"
              note="c-"
              go="4"
              ao="0"
              gidp="2"/>
      <batter id="474463" name="Anderson, B" name_display_first_last="Brett Anderson" pos="P"
              bo="802"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="460283" name="Blevins" name_display_first_last="Jerry Blevins" pos="P"
              bo="803"
              ab="1"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="1"
              avg=".000"
              ao="0"/>
      <batter id="519299" name="Sogard" name_display_first_last="Eric Sogard" pos="2B"
              bo="900"
              ab="2"
              po="2"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="0"
              lob="2"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="2"
              s_h="15"
              s_bb="5"
              s_r="8"
              s_so="10"
              avg=".231"
              ao="1"/>
      <batter id="489267" name="Rosales" name_display_first_last="Adam Rosales" pos="PH-2B"
              bo="901"
              ab="6"
              po="3"
              r="0"
              a="5"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="1"
              lob="3"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="1"
              s_h="4"
              s_bb="0"
              s_r="1"
              s_so="2"
              avg=".250"
              note="b-"
              go="3"
              ao="2"/>
      <batter id="573185" name="Straily" name_display_first_last="Dan Straily" pos="P" ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="450212" name="Neshek" name_display_first_last="Pat Neshek" pos="P" ab="0"
              po="0"
              r="0"
              a="1"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="434592" name="Resop" name_display_first_last="Chris Resop" pos="P" ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="448281" name="Doolittle" name_display_first_last="Sean Doolittle" pos="P"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="346797" name="Balfour" name_display_first_last="Grant Balfour" pos="P"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="475857" name="Cook" name_display_first_last="Ryan Cook" pos="P" ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <note><![CDATA[<span>a-Grounded out for Jaso in the 7th. b-Grounded out for Sogard in the 7th. c-Singled for Reddick in the 8th. </span>]]></note>
      <text_data><![CDATA[<b>BATTING</b><br/><span>
            <b>2B</b>: Lowrie (11, Williams).</span><br/><span>
            <b>3B</b>: Young, C (1, Williams).</span><br/><span>
            <b>HR</b>: Moss 2 (4, 6th inning off Hanson, 0 on, 2 out; 19th inning off Enright, 1 on, 2 out).</span><br/><span>
            <b>TB</b>: Young, C 4; Donaldson 3; Moss 9; Lowrie 3; Crisp; Cespedes; Smith, S 2; Rosales.</span><br/><span>
            <b>RBI</b>: Moss 3 (19), Lowrie (15), Donaldson 2 (20), Young, C (15), Cespedes (10), Rosales (1).</span><br/><span>
            <b>2-out RBI</b>: Moss 3; Young, C; Cespedes; Rosales.</span><br/><span>
            <b>Runners left in scoring position, 2 out</b>: Cespedes 2; Sogard; Rosales 2; Freiman.</span><br/><span>
            <b>GIDP</b>: Young, C 2.</span><br/><b>Team RISP</b>: 5-for-20.<br/><b>Team LOB</b>: 11.<br/><br/><b>BASERUNNING</b><br/><span>
            <b>SB</b>: Moss (1, 2nd base off Hanson/Iannetta), Donaldson (2, 2nd base off Hanson/Iannetta), Crisp (8, 3rd base off Frieri/Iannetta).</span><br/><br/><b>FIELDING</b><br/><span>
            <b>E</b>: Lowrie (5, fielding).</span><br/><span>
            <b>Outfield assists</b>: Reddick (Kendrick, H at 2nd base), Moss (Shuck at 2nd base).</span><br/><br/>]]></text_data>
      <note_es><![CDATA[<span>a-Bate&#243; por Jaso en la 7th. b-Bate&#243; por Sogard en la 7th. c-Bate&#243; por Reddick en la 8th. </span>]]></note_es>
      <text_data_es><![CDATA[<b>Bateo</b><br/><span>
            <b>2B</b>: Lowrie (11, Williams).</span><br/><span>
            <b>3B</b>: Young, C (1, Williams).</span><br/><span>
            <b>HR</b>: Moss 2 (4, 6th entrada ante Hanson, 0 en base, 2 out; 19th entrada ante Enright, 1 en base, 2 out).</span><br/><span>
            <b>BA</b>: Young, C 4; Donaldson 3; Moss 9; Lowrie 3; Crisp; Cespedes; Smith, S 2; Rosales.</span><br/><span>
            <b>RBI</b>: Moss 3 (19), Lowrie (15), Donaldson 2 (20), Young, C (15), Cespedes (10), Rosales (1).</span><br/><span>
            <b>2-out RBI</b>: Moss 3; Young, C; Cespedes; Rosales.</span><br/><span>
            <b>Corredores dejados en circulaci&#243;n, 2 out</b>: Cespedes 2; Sogard; Rosales 2; Freiman.</span><br/><span>
            <b>RDP</b>: Young, C 2.</span><br/><b>Equipo con Corredores en Posici&#243;n de Anotar</b>:
                        de 5-20.<br/><b>Equipo con Corredores Dejados en Circulaci&#243;n</b>: 11.<br/><br/><b>Corrido de Bases</b><br/><span>
            <b>SB</b>: Moss (1, 2nd base a Hanson/Iannetta), Donaldson (2, 2nd base a Hanson/Iannetta), Crisp (8, 3rd base a Frieri/Iannetta).</span><br/><br/><b>Defensa</b><br/><span>
            <b>E</b>: Lowrie (5, fielding).</span><br/><span>
            <b>Asistencias Desde los Jardines</b>: Reddick (Kendrick, H en 2nd base), Moss (Shuck en 2nd base).</span><br/><br/>]]></text_data_es>
   </batting>
   <pitching team_flag="home" out="57" h="15" r="8" er="8" bb="6" so="18" hr="3" bf="79"
             era="4.28">
      <pitcher id="573185" name="Straily" name_display_first_last="Dan Straily" pos="P"
               out="14"
               bf="23"
               er="6"
               r="6"
               h="7"
               so="6"
               hr="2"
               bb="1"
               np="88"
               s="55"
               w="1"
               l="0"
               sv="0"
               bs="0"
               hld="0"
               s_ip="11.1"
               s_h="12"
               s_r="8"
               s_er="8"
               s_bb="1"
               s_so="17"
               game_score="31"
               era="6.35"/>
      <pitcher id="450212" name="Neshek" name_display_first_last="Pat Neshek" pos="P" out="7"
               bf="9"
               er="1"
               r="1"
               h="1"
               so="2"
               hr="1"
               bb="1"
               np="28"
               s="19"
               w="0"
               l="0"
               sv="0"
               bs="0"
               hld="0"
               s_ip="11.1"
               s_h="13"
               s_r="6"
               s_er="4"
               s_bb="7"
               s_so="8"
               game_score="52"
               era="3.18"/>
      <pitcher id="434592" name="Resop" name_display_first_last="Chris Resop" pos="P" out="5"
               bf="7"
               er="0"
               r="0"
               h="1"
               so="1"
               hr="0"
               bb="1"
               np="34"
               s="19"
               w="1"
               l="0"
               sv="0"
               bs="0"
               hld="0"
               s_ip="12.2"
               s_h="16"
               s_r="7"
               s_er="6"
               s_bb="7"
               s_so="8"
               game_score="53"
               era="4.26"/>
      <pitcher id="448281" name="Doolittle" name_display_first_last="Sean Doolittle" pos="P"
               out="1"
               bf="1"
               er="0"
               r="0"
               h="0"
               so="1"
               hr="0"
               bb="0"
               np="4"
               s="3"
               w="1"
               l="0"
               sv="0"
               bs="1"
               hld="2"
               s_ip="10.0"
               s_h="5"
               s_r="2"
               s_er="2"
               s_bb="3"
               s_so="10"
               game_score="52"
               era="1.80"/>
      <pitcher id="346797" name="Balfour" name_display_first_last="Grant Balfour" pos="P"
               out="6"
               bf="9"
               er="0"
               r="0"
               h="2"
               so="2"
               hr="0"
               bb="1"
               np="31"
               s="20"
               w="0"
               l="0"
               sv="3"
               bs="0"
               hld="0"
               s_ip="11.0"
               s_h="10"
               s_r="3"
               s_er="3"
               s_bb="4"
               s_so="10"
               game_score="53"
               era="2.45"/>
      <pitcher id="475857" name="Cook" name_display_first_last="Ryan Cook" pos="P" out="3"
               bf="3"
               er="0"
               r="0"
               h="0"
               so="1"
               hr="0"
               bb="0"
               np="11"
               s="8"
               w="1"
               l="0"
               sv="0"
               bs="0"
               hld="3"
               s_ip="13.0"
               s_h="7"
               s_r="4"
               s_er="3"
               s_bb="6"
               s_so="14"
               game_score="54"
               era="2.08"/>
      <pitcher id="474463" name="Anderson, B" name_display_first_last="Brett Anderson" pos="P"
               out="16"
               bf="21"
               er="1"
               r="1"
               h="3"
               so="5"
               hr="0"
               bb="2"
               np="79"
               s="49"
               w="1"
               l="4"
               sv="0"
               bs="0"
               hld="0"
               s_ip="29.0"
               s_h="32"
               s_r="22"
               s_er="20"
               s_bb="15"
               s_so="29"
               game_score="61"
               era="6.21"/>
      <pitcher id="460283" name="Blevins" name_display_first_last="Jerry Blevins" pos="P"
               out="5"
               bf="6"
               er="0"
               r="0"
               h="1"
               so="0"
               hr="0"
               bb="0"
               np="25"
               s="15"
               w="2"
               l="0"
               sv="0"
               bs="1"
               hld="0"
               s_ip="16.1"
               s_h="10"
               s_r="3"
               s_er="3"
               s_bb="1"
               s_so="16"
               game_score="53"
               era="1.65"
               win="true"
               note="(W, 2-0)"/>
   </pitching>
   <batting team_flag="away" ab="70" r="8" h="15" d="2" t="0" hr="3" rbi="8" bb="6" po="56"
            da="20"
            so="18"
            lob="22"
            avg=".263">
      <batter id="488721" name="Bourjos" name_display_first_last="Peter Bourjos" pos="CF"
              bo="100"
              ab="4"
              po="1"
              r="1"
              a="0"
              bb="0"
              sac="1"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="1"
              so="2"
              hr="0"
              rbi="0"
              lob="1"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="2"
              s_rbi="8"
              s_h="26"
              s_bb="4"
              s_r="12"
              s_so="20"
              avg=".313"
              go="1"
              ao="2"/>
      <batter id="543776" name="Shuck" name_display_first_last="J.B. Shuck" pos="LF" bo="101"
              ab="2"
              po="0"
              r="0"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="1"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="2"
              s_h="6"
              s_bb="2"
              s_r="1"
              s_so="3"
              avg=".429"
              go="1"
              ao="0"/>
      <batter id="545361" name="Trout" name_display_first_last="Mike Trout" pos="LF-CF"
              bo="200"
              ab="8"
              po="7"
              r="1"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="2"
              hr="0"
              rbi="0"
              lob="5"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="2"
              s_rbi="12"
              s_h="27"
              s_bb="12"
              s_r="14"
              s_so="25"
              avg=".252"
              go="3"
              ao="2"/>
      <batter id="405395" name="Pujols" name_display_first_last="Albert Pujols" pos="1B"
              bo="300"
              ab="8"
              po="15"
              r="3"
              a="4"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="4"
              e="1"
              d="0"
              hbp="0"
              so="0"
              hr="2"
              rbi="3"
              lob="1"
              fldg=".950"
              sb="0"
              cs="0"
              s_hr="4"
              s_rbi="16"
              s_h="26"
              s_bb="15"
              s_r="12"
              s_so="12"
              avg=".265"
              go="1"
              ao="3"/>
      <batter id="285078" name="Hamilton" name_display_first_last="Josh Hamilton" pos="RF"
              bo="400"
              ab="8"
              po="7"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="1"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="3"
              hr="0"
              rbi="1"
              lob="4"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="2"
              s_rbi="9"
              s_h="21"
              s_bb="5"
              s_r="10"
              s_so="32"
              avg=".202"
              go="1"
              ao="5"/>
      <batter id="444432" name="Trumbo" name_display_first_last="Mark Trumbo" pos="DH"
              bo="500"
              ab="8"
              po="0"
              r="1"
              a="0"
              bb="1"
              sac="0"
              t="0"
              sf="0"
              h="3"
              e="0"
              d="1"
              hbp="0"
              so="2"
              hr="1"
              rbi="3"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="4"
              s_rbi="15"
              s_h="32"
              s_bb="8"
              s_r="12"
              s_so="28"
              avg=".302"
              go="3"
              ao="0"/>
      <batter id="435062" name="Kendrick, H" name_display_first_last="Howie Kendrick"
              pos="2B"
              bo="600"
              ab="9"
              po="4"
              r="0"
              a="5"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="2"
              e="1"
              d="0"
              hbp="0"
              so="2"
              hr="0"
              rbi="0"
              lob="3"
              fldg=".900"
              sb="0"
              cs="0"
              s_hr="3"
              s_rbi="14"
              s_h="28"
              s_bb="6"
              s_r="8"
              s_so="17"
              avg=".283"
              go="3"
              ao="2"/>
      <batter id="430593" name="Harris, B" name_display_first_last="Brendan Harris"
              pos="SS-3B"
              bo="700"
              ab="9"
              po="2"
              r="1"
              a="6"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="2"
              e="1"
              d="1"
              hbp="0"
              so="2"
              hr="0"
              rbi="0"
              lob="3"
              fldg=".889"
              sb="0"
              cs="0"
              s_hr="1"
              s_rbi="4"
              s_h="14"
              s_bb="2"
              s_r="6"
              s_so="12"
              avg=".264"
              go="3"
              ao="2"/>
      <batter id="455104" name="Iannetta" name_display_first_last="Chris Iannetta" pos="C"
              bo="800"
              ab="6"
              po="18"
              r="0"
              a="0"
              bb="2"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="2"
              hr="0"
              rbi="0"
              lob="1"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="3"
              s_rbi="9"
              s_h="16"
              s_bb="11"
              s_r="11"
              s_so="19"
              avg=".225"
              ao="4"/>
      <batter id="499864" name="Jimenez, L" name_display_first_last="Luis Jimenez" pos="3B"
              bo="900"
              ab="3"
              po="0"
              r="1"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="1"
              hr="0"
              rbi="0"
              lob="1"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="2"
              s_h="15"
              s_bb="2"
              s_r="10"
              s_so="20"
              avg=".273"
              ao="1"/>
      <batter id="461865" name="Romine, A" name_display_first_last="Andrew Romine" pos="SS"
              bo="901"
              ab="5"
              po="0"
              r="0"
              a="3"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="1"
              e="0"
              d="0"
              hbp="0"
              so="2"
              hr="0"
              rbi="0"
              lob="3"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="1"
              s_h="3"
              s_bb="1"
              s_r="1"
              s_so="6"
              avg=".130"
              go="1"
              ao="1"/>
      <batter id="462102" name="Hanson" name_display_first_last="Tommy Hanson" pos="P" ab="0"
              po="2"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="607706" name="Roth" name_display_first_last="Michael Roth" pos="P" ab="0"
              po="0"
              r="0"
              a="1"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="451773" name="De La Rosa, D" name_display_first_last="Dane De La Rosa"
              pos="P"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="275933" name="Downs, S" name_display_first_last="Scott Downs" pos="P"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="457117" name="Frieri" name_display_first_last="Ernesto Frieri" pos="P"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="425532" name="Williams" name_display_first_last="Jerome Williams" pos="P"
              ab="0"
              po="0"
              r="0"
              a="1"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg="1.000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="543409" name="Kohn" name_display_first_last="Michael Kohn" pos="P" ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <batter id="446264" name="Enright" name_display_first_last="Barry Enright" pos="P"
              ab="0"
              po="0"
              r="0"
              a="0"
              bb="0"
              sac="0"
              t="0"
              sf="0"
              h="0"
              e="0"
              d="0"
              hbp="0"
              so="0"
              hr="0"
              rbi="0"
              lob="0"
              fldg=".000"
              sb="0"
              cs="0"
              s_hr="0"
              s_rbi="0"
              s_h="0"
              s_bb="0"
              s_r="0"
              s_so="0"
              avg=".000"
              ao="0"/>
      <text_data><![CDATA[<b>BATTING</b><br/><span>
            <b>2B</b>: Trumbo (8, Straily), Harris, B (4, Anderson, B).</span><br/><span>
            <b>HR</b>: Pujols 2 (4, 1st inning off Straily, 0 on, 2 out; 7th inning off Neshek, 0 on, 1 out), Trumbo (4, 2nd inning off Straily, 0 on, 0 out).</span><br/><span>
            <b>TB</b>: Shuck; Trout; Harris, B 3; Kendrick, H 2; Jimenez, L; Trumbo 7; Romine, A; Pujols 10.</span><br/><span>
            <b>RBI</b>: Pujols 3 (16), Trumbo 3 (15), Hamilton (9), Shuck (2).</span><br/><span>
            <b>2-out RBI</b>: Pujols; Trumbo 2; Shuck.</span><br/><span>
            <b>Runners left in scoring position, 2 out</b>: Harris, B; Kendrick, H; Hamilton 2; Trout 2.</span><br/><span>
            <b>SAC</b>: Bourjos.</span><br/><span>
            <b>SF</b>: Hamilton.</span><br/><b>Team RISP</b>: 3-for-10.<br/><b>Team LOB</b>: 14.<br/><br/><b>FIELDING</b><br/><span>
            <b>E</b>: Harris, B (2, interference), Kendrick, H (5, fielding), Pujols (2, missed catch).</span><br/><span>
            <b>PB</b>: Iannetta (2).</span><br/><span>
            <b>DP</b>: 2 (Romine, A-Kendrick, H-Pujols, Harris, B-Pujols).</span><br/><br/>]]></text_data>
      <text_data_es><![CDATA[<b>Bateo</b><br/><span>
            <b>2B</b>: Trumbo (8, Straily), Harris, B (4, Anderson, B).</span><br/><span>
            <b>HR</b>: Pujols 2 (4, 1st entrada ante Straily, 0 en base, 2 out; 7th entrada ante Neshek, 0 en base, 1 out), Trumbo (4, 2nd entrada ante Straily, 0 en base, 0 out).</span><br/><span>
            <b>BA</b>: Shuck; Trout; Harris, B 3; Kendrick, H 2; Jimenez, L; Trumbo 7; Romine, A; Pujols 10.</span><br/><span>
            <b>RBI</b>: Pujols 3 (16), Trumbo 3 (15), Hamilton (9), Shuck (2).</span><br/><span>
            <b>2-out RBI</b>: Pujols; Trumbo 2; Shuck.</span><br/><span>
            <b>Corredores dejados en circulaci&#243;n, 2 out</b>: Harris, B; Kendrick, H; Hamilton 2; Trout 2.</span><br/><span>
            <b>SAC</b>: Bourjos.</span><br/><span>
            <b>SF</b>: Hamilton.</span><br/><b>Equipo con Corredores en Posici&#243;n de Anotar</b>:
                        de 3-10.<br/><b>Equipo con Corredores Dejados en Circulaci&#243;n</b>: 14.<br/><br/><b>Defensa</b><br/><span>
            <b>E</b>: Harris, B (2, interference), Kendrick, H (5, fielding), Pujols (2, missed catch).</span><br/><span>
            <b>PB</b>: Iannetta (2).</span><br/><span>
            <b>DP</b>: 2 (Romine, A-Kendrick, H-Pujols, Harris, B-Pujols).</span><br/><br/>]]></text_data_es>
   </batting>
   <game_info><![CDATA[<span>Roth pitched to 3 batters in the 8th.</span><br/><span>Downs, S pitched to 1 batter in the 8th.</span><br/><br/><span>
         <b>Game Scores</b>: Hanson 63, Straily 31.</span><br/><span>
         <b>IBB</b>: Pujols (by Balfour), Iannetta (by Anderson, B).</span><br/><span>
         <b>HBP</b>: Bourjos (by Straily).</span><br/><span>
         <b>Pitches-strikes</b>: Hanson 100-65, Roth 23-13, De La Rosa, D 11-5, Downs, S 4-2, Frieri 27-17, Williams 73-45, Kohn 31-20, Enright 28-18, Straily 88-55, Neshek 28-19, Resop 34-19, Doolittle 4-3, Balfour 31-20, Cook 11-8, Anderson, B 79-49, Blevins 25-15.</span><br/><span>
         <b>Groundouts-flyouts</b>: Hanson 7-2, Roth 3-0, De La Rosa, D 1-0, Downs, S 0-0, Frieri 0-2, Williams 7-5, Kohn 1-1, Enright 1-1, Straily 3-3, Neshek 1-0, Resop 1-1, Doolittle 0-0, Balfour 1-2, Cook 2-0, Anderson, B 7-4, Blevins 2-2.</span><br/><span>
         <b>Batters faced</b>: Hanson 24, Roth 6, De La Rosa, D 4, Downs, S 1, Frieri 6, Williams 23, Kohn 6, Enright 7, Straily 23, Neshek 9, Resop 7, Doolittle 1, Balfour 9, Cook 3, Anderson, B 21, Blevins 6.</span><br/><span>
         <b>Inherited runners-scored</b>: De La Rosa, D 2-1, Downs, S 2-1, Frieri 2-0, Neshek 1-0, Doolittle 2-0, Blevins 1-0.</span><br/><b>Umpires</b>: HP: Kerwin Danley. 1B: Vic Carapazza. 2B: Gary Cederstrom. 3B: Lance Barksdale. <br/><b>Weather</b>: 71 degrees, partly cloudy.<br/><b>Wind</b>: 16 mph, Out to RF.<br/><b>T</b>: 6:32.<br/><b>Att</b>: 11,668.<br/><b>Venue</b>: O.co Coliseum.<br/><b>April 29, 2013</b><br/>]]></game_info>
   <game_info_es><![CDATA[<span>Roth enfrent&#243; 3 bateadores en la 8th.</span><br/><span>Downs, S enfrent&#243; 1 bateador en la 8th.</span><br/><br/><span>
         <b>Anotaciones del Juego</b>: Hanson 63, Straily 31.</span><br/><span>
         <b>BBI</b>: Pujols (por Balfour), Iannetta (por Anderson, B).</span><br/><span>
         <b>BG</b>: Bourjos (por Straily).</span><br/><span>
         <b>Lanzamientos-strikes</b>: Hanson 100-65, Roth 23-13, De La Rosa, D 11-5, Downs, S 4-2, Frieri 27-17, Williams 73-45, Kohn 31-20, Enright 28-18, Straily 88-55, Neshek 28-19, Resop 34-19, Doolittle 4-3, Balfour 31-20, Cook 11-8, Anderson, B 79-49, Blevins 25-15.</span><br/><span>
         <b>Roletazos-elevados de out</b>: Hanson 7-2, Roth 3-0, De La Rosa, D 1-0, Downs, S 0-0, Frieri 0-2, Williams 7-5, Kohn 1-1, Enright 1-1, Straily 3-3, Neshek 1-0, Resop 1-1, Doolittle 0-0, Balfour 1-2, Cook 2-0, Anderson, B 7-4, Blevins 2-2.</span><br/><span>
         <b>Bateadores enfrentados</b>: Hanson 24, Roth 6, De La Rosa, D 4, Downs, S 1, Frieri 6, Williams 23, Kohn 6, Enright 7, Straily 23, Neshek 9, Resop 7, Doolittle 1, Balfour 9, Cook 3, Anderson, B 21, Blevins 6.</span><br/><span>
         <b>Corredores Heredados que Anotaron</b>: De La Rosa, D 2-1, Downs, S 2-1, Frieri 2-0, Neshek 1-0, Doolittle 2-0, Blevins 1-0.</span><br/><b>&#193;rbitros</b>: HP: Kerwin Danley. 1B: Vic Carapazza. 2B: Gary Cederstrom. 3B: Lance Barksdale. <br/><b>Clima</b>: 71 degrees, partly cloudy.<br/><b>Viento</b>: 16 mph, Out to RF.<br/><b>T</b>: 6:32.<br/><b>Att</b>: 11,668.<br/><b>Estadio</b>: O.co Coliseum.<br/><b>April 29, 2013</b><br/>]]></game_info_es>
</boxscore>
    """
    XML_GAME = """
<!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt--><game type="R" local_game_time="19:05" game_pk="347121" game_time_et="10:05 PM" gameday_sw="P">
	<team type="home" code="oak" file_code="oak" abbrev="OAK" id="133" name="Oakland" name_full="Oakland Athletics" name_brief="Athletics" w="15" l="12" division_id="200" league_id="103" league="AL"/>
	<team type="away" code="ana" file_code="ana" abbrev="LAA" id="108" name="LA Angels" name_full="Los Angeles Angels" name_brief="Angels" w="9" l="16" division_id="200" league_id="103" league="AL"/>
	<stadium id="10" name="O.co Coliseum" venue_w_chan_loc="USCA0791" location="Oakland, CA"/>
</game>
    """
    XML_PLAYERS = """
<!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt--><game venue="O.co Coliseum" date="April 29, 2013">
	<team type="away" id="LAA" name="Los Angeles Angels">
		<player id="275933" first="Scott" last="Downs" num="37" boxname="Downs, S" rl="L" bats="L" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="2" era="2.53"/>
		<player id="285078" first="Josh" last="Hamilton" num="32" boxname="Hamilton" rl="L" bats="L" position="LF" current_position="RF" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="4" game_position="RF" avg=".219" hr="2" rbi="8"/>
		<player id="405395" first="Albert" last="Pujols" num="5" boxname="Pujols" rl="R" bats="R" position="1B" current_position="1B" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="3" game_position="1B" avg=".244" hr="2" rbi="13"/>
		<player id="425492" first="Ryan" last="Madson" num="46" boxname="Madson" rl="R" bats="L" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="-"/>
		<player id="425532" first="Jerome" last="Williams" num="57" boxname="Williams" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="2.35"/>
		<player id="430593" first="Brendan" last="Harris" num="20" boxname="Harris, B" rl="R" bats="R" position="SS" current_position="3B" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="7" game_position="SS" avg=".273" hr="1" rbi="4"/>
		<player id="430599" first="Joe" last="Blanton" num="55" boxname="Blanton" rl="R" bats="R" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="4" era="7.09"/>
		<player id="430634" first="Sean" last="Burnett" num="24" boxname="Burnett, S" rl="L" bats="L" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="1.04"/>
		<player id="430947" first="Erick" last="Aybar" num="2" boxname="Aybar" rl="R" bats="S" position="SS" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".321" hr="0" rbi="1"/>
		<player id="430948" first="Alberto" last="Callaspo" num="6" boxname="Callaspo" rl="R" bats="S" position="3B" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".273" hr="1" rbi="3"/>
		<player id="435062" first="Howie" last="Kendrick" num="47" boxname="Kendrick, H" rl="R" bats="R" position="2B" current_position="2B" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="6" game_position="2B" avg=".289" hr="3" rbi="14"/>
		<player id="444432" first="Mark" last="Trumbo" num="44" boxname="Trumbo" rl="R" bats="R" position="1B" current_position="DH" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="5" game_position="DH" avg=".296" hr="3" rbi="12"/>
		<player id="446264" first="Barry" last="Enright" num="45" boxname="Enright" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="-"/>
		<player id="448178" first="Kevin" last="Jepsen" num="40" boxname="Jepsen" rl="R" bats="R" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="1" era="9.82"/>
		<player id="450275" first="Mark" last="Lowe" num="38" boxname="Lowe, M" rl="R" bats="L" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="11.37"/>
		<player id="450306" first="Jason" last="Vargas" num="60" boxname="Vargas" rl="L" bats="L" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="3" era="4.85"/>
		<player id="450308" first="Jered" last="Weaver" num="36" boxname="Weaver" rl="R" bats="R" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="1" era="4.91"/>
		<player id="450351" first="C.J." last="Wilson" num="33" boxname="Wilson, C" rl="L" bats="L" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="2" losses="0" era="4.30"/>
		<player id="451773" first="Dane" last="De La Rosa" num="65" boxname="De La Rosa, D" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="2.31"/>
		<player id="455104" first="Chris" last="Iannetta" num="17" boxname="Iannetta" rl="R" bats="R" position="C" current_position="C" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="8" game_position="C" avg=".246" hr="3" rbi="9"/>
		<player id="457117" first="Ernesto" last="Frieri" num="49" boxname="Frieri" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="1" era="1.93"/>
		<player id="461865" first="Andrew" last="Romine" num="7" boxname="Romine, A" rl="R" bats="S" position="SS" current_position="SS" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".111" hr="0" rbi="1"/>
		<player id="462102" first="Tommy" last="Hanson" num="48" boxname="Hanson" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="0" game_position="P" avg=".000" hr="0" rbi="0" wins="2" losses="1" era="4.24"/>
		<player id="474233" first="Hank" last="Conger" num="16" boxname="Conger" rl="R" bats="S" position="C" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".227" hr="1" rbi="3"/>
		<player id="476531" first="Andrew" last="Taylor" num="64" boxname="Taylor, A" rl="L" bats="R" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="-"/>
		<player id="488721" first="Peter" last="Bourjos" num="25" boxname="Bourjos" rl="R" bats="R" position="CF" current_position="CF" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="1" game_position="CF" avg=".329" hr="2" rbi="8"/>
		<player id="499864" first="Luis" last="Jimenez" num="18" boxname="Jimenez, L" rl="R" bats="R" position="3B" current_position="3B" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="9" game_position="3B" avg=".269" hr="0" rbi="2"/>
		<player id="543409" first="Michael" last="Kohn" num="58" boxname="Kohn" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="9.00"/>
		<player id="543488" first="Nick" last="Maronde" num="63" boxname="Maronde" rl="L" bats="S" position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="3.86"/>
		<player id="543776" first="J.B." last="Shuck" num="39" boxname="Shuck" rl="L" bats="L" position="LF" current_position="LF" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".417" hr="0" rbi="1"/>
		<player id="545361" first="Mike" last="Trout" num="27" boxname="Trout" rl="R" bats="R" position="CF" current_position="CF" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" bat_order="2" game_position="LF" avg=".263" hr="2" rbi="12"/>
		<player id="607706" first="Michael" last="Roth" num="51" boxname="Roth" rl="L" bats="L" position="P" current_position="P" status="A" team_abbrev="LAA" team_id="108" parent_team_abbrev="LAA" parent_team_id="108" avg=".000" hr="0" rbi="0" wins="1" losses="1" era="7.27"/>
<coach position="manager" first="Mike" last="Scioscia" id="121919" num="14"/><coach position="batting_coach" first="Jim" last="Eppard" id="113867" num="80"/><coach position="pitching_coach" first="Mike" last="Butcher" id="111807" num="23"/><coach position="first_base_coach" first="Alfredo" last="Griffin" id="115137" num="4"/><coach position="third_base_coach" first="Dino" last="Ebel" id="492822" num="21"/><coach position="bench_coach" first="Rob" last="Picciolo" id="120537" num="9"/><coach position="infield_coach" first="Bobby" last="Knoop" id="117202" num="1"/><coach position="bullpen_coach" first="Steve" last="Soliz" id="150354" num="61"/><coach position="bullpen_catcher" first="Tom" last="Gregorio" id="408054" num="70"/><coach position="catching_coach" first="Bill" last="Lachemann" id="628306" num=""/><coach position="coach" first="Shayne" last="Kelley" id="648317" num=""/>	</team>
	<team type="home" id="OAK" name="Oakland Athletics">
		<player id="112526" first="Bartolo" last="Colon" num="40" boxname="Colon" rl="R" bats="R" position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="3" losses="0" era="3.38"/>
		<player id="346797" first="Grant" last="Balfour" num="50" boxname="Balfour" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="3.00"/>
		<player id="424825" first="Coco" last="Crisp" num="4" boxname="Crisp" rl="R" bats="S" position="CF" current_position="CF" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="1" game_position="CF" avg=".290" hr="5" rbi="12"/>
		<player id="434592" first="Chris" last="Resop" num="44" boxname="Resop" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="4.91"/>
		<player id="444379" first="John" last="Jaso" num="5" boxname="Jaso" rl="R" bats="L" position="C" current_position="C" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="7" game_position="C" avg=".267" hr="1" rbi="9"/>
		<player id="448281" first="Sean" last="Doolittle" num="62" boxname="Doolittle" rl="L" bats="L" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="1.86"/>
		<player id="450212" first="Pat" last="Neshek" num="47" boxname="Neshek" rl="R" bats="S" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="3.00"/>
		<player id="451775" first="Fernando" last="Rodriguez" num="33" boxname="Rodriguez, Fe" rl="R" bats="R" position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="-"/>
		<player id="452234" first="Seth" last="Smith" num="15" boxname="Smith, S" rl="L" bats="L" position="LF" current_position="LF" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="2" game_position="DH" avg=".319" hr="3" rbi="13"/>
		<player id="455759" first="Chris" last="Young" num="25" boxname="Young, C" rl="R" bats="R" position="CF" current_position="CF" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".157" hr="4" rbi="14"/>
		<player id="456167" first="A.J." last="Griffin" num="64" boxname="Griffin" rl="R" bats="R" position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="2" losses="2" era="4.65"/>
		<player id="460283" first="Jerry" last="Blevins" num="13" boxname="Blevins" rl="L" bats="L" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="1.84"/>
		<player id="461235" first="Brandon" last="Moss" num="37" boxname="Moss" rl="R" bats="L" position="1B" current_position="RF" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="5" game_position="1B" avg=".289" hr="2" rbi="16"/>
		<player id="474384" first="Nate" last="Freiman" num="7" boxname="Freiman" rl="R" bats="R" position="1B" current_position="1B" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".160" hr="1" rbi="5"/>
		<player id="474463" first="Brett" last="Anderson" num="49" boxname="Anderson, B" rl="L" bats="L" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="1" losses="4" era="7.23"/>
		<player id="475857" first="Ryan" last="Cook" num="48" boxname="Cook" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="2.25"/>
		<player id="476704" first="Jed" last="Lowrie" num="8" boxname="Lowrie" rl="R" bats="S" position="SS" current_position="SS" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="3" game_position="SS" avg=".344" hr="3" rbi="14"/>
		<player id="489267" first="Adam" last="Rosales" num="17" boxname="Rosales" rl="R" bats="R" position="SS" current_position="2B" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".300" hr="0" rbi="0"/>
		<player id="493141" first="Hiroyuki" last="Nakajima" num="3" boxname="Nakajima" rl="R" bats="R" position="SS" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0"/>
		<player id="493316" first="Yoenis" last="Cespedes" num="52" boxname="Cespedes" rl="R" bats="R" position="LF" current_position="CF" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="4" game_position="LF" avg=".222" hr="4" rbi="9"/>
		<player id="502003" first="Scott" last="Sizemore" num="29" boxname="Sizemore" rl="R" bats="R" position="2B" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".167" hr="0" rbi="0"/>
		<player id="502210" first="Josh" last="Reddick" num="16" boxname="Reddick" rl="R" bats="L" position="RF" current_position="RF" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="8" game_position="RF" avg=".153" hr="1" rbi="13"/>
		<player id="518626" first="Josh" last="Donaldson" num="20" boxname="Donaldson" rl="R" bats="R" position="3B" current_position="3B" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="6" game_position="3B" avg=".319" hr="2" rbi="18"/>
		<player id="519083" first="Derek" last="Norris" num="36" boxname="Norris, D" rl="R" bats="R" position="C" current_position="C" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".289" hr="0" rbi="4"/>
		<player id="519105" first="Jarrod" last="Parker" num="11" boxname="Parker" rl="R" bats="R" position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="0" losses="4" era="8.10"/>
		<player id="519299" first="Eric" last="Sogard" num="28" boxname="Sogard" rl="R" bats="L" position="2B" current_position="2B" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="9" game_position="2B" avg=".238" hr="0" rbi="2"/>
		<player id="543548" first="Tommy" last="Milone" num="57" boxname="Milone" rl="L" bats="L" position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" avg=".000" hr="0" rbi="0" wins="3" losses="2" era="3.38"/>
		<player id="573185" first="Dan" last="Straily" num="67" boxname="Straily" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="OAK" team_id="133" parent_team_abbrev="OAK" parent_team_id="133" bat_order="0" game_position="P" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="2.70"/>
<coach position="manager" first="Bob" last="Melvin" id="118942" num="6"/><coach position="hitting_coach" first="Chili" last="Davis" id="113099" num="30"/><coach position="pitching_coach" first="Curt" last="Young" id="124689" num="41"/><coach position="first_base_coach" first="Tye" last="Waller" id="123868" num="46"/><coach position="third_base_coach" first="Mike" last="Gallego" id="114545" num="2"/><coach position="bench_coach" first="Chip" last="Hale" id="115330" num="14"/><coach position="bullpen_coach" first="Darren" last="Bush" id="470252" num="51"/><coach position="coach" first="Ariel" last="Prieto" id="120768" num="59"/>	</team>
<umpires><umpire position="home" name="Kerwin Danley" id="427095" first="Kerwin" last="Danley"/><umpire position="first" name="Vic Carapazza" id="483569" first="Vic" last="Carapazza"/><umpire position="second" name="Gary Cederstrom" id="427058" first="Gary" last="Cederstrom"/><umpire position="third" name="Lance Barksdale" id="427013" first="Lance" last="Barksdale"/></umpires></game>
    """

    def setUp(self):
        self.game = Game._generate_game_object(
            BeautifulSoup(TestBoxScore.XML_GAME, 'lxml'),
            dt.strptime('2013-04-29', '%Y-%m-%d'),
            1
        )
        self.players = Players._read_objects(BeautifulSoup(TestBoxScore.XML_PLAYERS, 'lxml'), self.game)

    def tearDown(self):
        pass

    def test_generate_object(self):
        """
        Box Score Data Test
        """
        soup = BeautifulSoup(TestBoxScore.XML_BOXSCORE, 'lxml')
        boxscore = BoxScore._generate_object(soup, self.game, self.players)
        self.assertEqual(boxscore.retro_game_id, 'OAK201304290')
        self.assertEqual(boxscore.home_team_id, 'oak')
        self.assertEqual(boxscore.away_team_id, 'ana')
        self.assertEqual(len(boxscore.home_batting), 21)
        self.assertEqual(len(boxscore.away_batting), 19)
        self.assertEqual(len(boxscore.home_pitching), 8)
        self.assertEqual(len(boxscore.away_pitching), 8)

    def test_row(self):
        """
        Box Score Row Data Test
        """
        soup = BeautifulSoup(TestBoxScore.XML_BOXSCORE, 'lxml')
        boxscore = BoxScore._generate_object(soup, self.game, self.players)
        row = boxscore.row()
        self.assertEqual(len(row), 61)
        self.assertEqual(row['retro_game_id'], 'OAK201304290')
        self.assertEqual(row['home_team_id'], 'oak')
        self.assertEqual(row['away_team_id'], 'ana')
        self.assertEqual(row['home_lineup_1_id'], '424825')
        self.assertEqual(row['home_lineup_1_name'], 'Crisp')
        self.assertEqual(row['home_lineup_1_pos'], 'CF')
        self.assertEqual(row['home_lineup_2_id'], '452234')
        self.assertEqual(row['home_lineup_2_name'], 'Smith, S')
        self.assertEqual(row['home_lineup_2_pos'], 'DH-LF')
        self.assertEqual(row['home_lineup_3_id'], '476704')
        self.assertEqual(row['home_lineup_3_name'], 'Lowrie')
        self.assertEqual(row['home_lineup_3_pos'], 'SS')
        self.assertEqual(row['home_lineup_4_id'], '493316')
        self.assertEqual(row['home_lineup_4_name'], 'Cespedes')
        self.assertEqual(row['home_lineup_4_pos'], 'LF-CF')
        self.assertEqual(row['home_lineup_5_id'], '461235')
        self.assertEqual(row['home_lineup_5_name'], 'Moss')
        self.assertEqual(row['home_lineup_5_pos'], '1B-RF')
        self.assertEqual(row['home_lineup_6_id'], '518626')
        self.assertEqual(row['home_lineup_6_name'], 'Donaldson')
        self.assertEqual(row['home_lineup_6_pos'], '3B')
        self.assertEqual(row['home_lineup_7_id'], '444379')
        self.assertEqual(row['home_lineup_7_name'], 'Jaso')
        self.assertEqual(row['home_lineup_7_pos'], 'C')
        self.assertEqual(row['home_lineup_8_id'], '502210')
        self.assertEqual(row['home_lineup_8_name'], 'Reddick')
        self.assertEqual(row['home_lineup_8_pos'], 'RF')
        self.assertEqual(row['home_lineup_9_id'], '519299')
        self.assertEqual(row['home_lineup_9_name'], 'Sogard')
        self.assertEqual(row['home_lineup_9_pos'], '2B')
        self.assertEqual(len(json.loads(row['home_batter'])), 21)
        self.assertEqual(len(json.loads(row['home_pitcher'])), 8)

        self.assertEqual(row['away_lineup_1_id'], '488721')
        self.assertEqual(row['away_lineup_1_name'], 'Bourjos')
        self.assertEqual(row['away_lineup_1_pos'], 'CF')
        self.assertEqual(row['away_lineup_2_id'], '545361')
        self.assertEqual(row['away_lineup_2_name'], 'Trout')
        self.assertEqual(row['away_lineup_2_pos'], 'LF-CF')
        self.assertEqual(row['away_lineup_3_id'], '405395')
        self.assertEqual(row['away_lineup_3_name'], 'Pujols')
        self.assertEqual(row['away_lineup_3_pos'], '1B')
        self.assertEqual(row['away_lineup_4_id'], '285078')
        self.assertEqual(row['away_lineup_4_name'], 'Hamilton')
        self.assertEqual(row['away_lineup_4_pos'], 'RF')
        self.assertEqual(row['away_lineup_5_id'], '444432')
        self.assertEqual(row['away_lineup_5_name'], 'Trumbo')
        self.assertEqual(row['away_lineup_5_pos'], 'DH')
        self.assertEqual(row['away_lineup_6_id'], '435062')
        self.assertEqual(row['away_lineup_6_name'], 'Kendrick, H')
        self.assertEqual(row['away_lineup_6_pos'], '2B')
        self.assertEqual(row['away_lineup_7_id'], '430593')
        self.assertEqual(row['away_lineup_7_name'], 'Harris, B')
        self.assertEqual(row['away_lineup_7_pos'], 'SS-3B')
        self.assertEqual(row['away_lineup_8_id'], '455104')
        self.assertEqual(row['away_lineup_8_name'], 'Iannetta')
        self.assertEqual(row['away_lineup_8_pos'], 'C')
        self.assertEqual(row['away_lineup_9_id'], '499864')
        self.assertEqual(row['away_lineup_9_name'], 'Jimenez, L')
        self.assertEqual(row['away_lineup_9_pos'], '3B')
        self.assertEqual(len(json.loads(row['away_batter'])), 19)
        self.assertEqual(len(json.loads(row['away_pitcher'])), 8)

    def test_get_batter(self):
        """
        Batter Profile
        """
        soup = BeautifulSoup(TestBoxScore.XML_BOXSCORE, 'lxml')
        boxscore = BoxScore._generate_object(soup, self.game, self.players)
        home_batters = soup.find('batting', attrs={'team_flag': 'home'}).find_all('batter')
        crisp = boxscore._get_batter(home_batters[0])
        self.assertEqual(crisp.get('bo'), '1')
        self.assertEqual(crisp.get('pos'), 'CF')
        self.assertEqual(crisp.get('id'), '424825')
        self.assertEqual(crisp.get('first'), 'Coco')
        self.assertEqual(crisp.get('last'), 'Crisp')
        self.assertEqual(crisp.get('box_name'), 'Crisp')
        self.assertEqual(crisp.get('rl'), 'R')
        self.assertEqual(crisp.get('bats'), 'S')
        self.assertTrue(crisp.get('starting'))

        away_batters = soup.find('batting', attrs={'team_flag': 'away'}).find_all('batter')
        shuck = boxscore._get_batter(away_batters[1])
        self.assertEqual(shuck.get('bo'), '1')
        self.assertEqual(shuck.get('pos'), 'LF')
        self.assertEqual(shuck.get('id'), '543776')
        self.assertEqual(shuck.get('first'), 'J.B.')
        self.assertEqual(shuck.get('last'), 'Shuck')
        self.assertEqual(shuck.get('box_name'), 'Shuck')
        self.assertEqual(shuck.get('rl'), 'L')
        self.assertEqual(shuck.get('bats'), 'L')
        self.assertFalse(shuck.get('starting'))

    def test_get_pitcher(self):
        """
        Pitcher Profile
        """
        soup = BeautifulSoup(TestBoxScore.XML_BOXSCORE, 'lxml')
        boxscore = BoxScore._generate_object(soup, self.game, self.players)
        home_pitchers = soup.find('pitching', attrs={'team_flag': 'home'}).find_all('pitcher')
        straily = boxscore._get_pitcher(home_pitchers[0])
        self.assertEqual(straily.get('pos'), 'P')
        self.assertEqual(straily.get('id'), '573185')
        self.assertEqual(straily.get('first'), 'Dan')
        self.assertEqual(straily.get('last'), 'Straily')
        self.assertEqual(straily.get('box_name'), 'Straily')
        self.assertEqual(straily.get('rl'), 'R')
        self.assertEqual(straily.get('bats'), 'R')
        self.assertEqual(straily.get('out'), '14')
        self.assertEqual(straily.get('bf'), '23')

        away_pitchers = soup.find('pitching', attrs={'team_flag': 'away'}).find_all('pitcher')
        enright = boxscore._get_pitcher(away_pitchers[7])
        self.assertEqual(enright.get('pos'), 'P')
        self.assertEqual(enright.get('id'), '446264')
        self.assertEqual(enright.get('first'), 'Barry')
        self.assertEqual(enright.get('last'), 'Enright')
        self.assertEqual(enright.get('box_name'), 'Enright')
        self.assertEqual(enright.get('rl'), 'R')
        self.assertEqual(enright.get('bats'), 'R')
        self.assertEqual(enright.get('out'), '5')
        self.assertEqual(enright.get('bf'), '7')

    def test_get_batting_order_starting_flg(self):
        """
        Batting order number & starting flag
        """
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': '100'})
        self.assertEqual(bo, '1')
        self.assertTrue(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': '201'})
        self.assertEqual(bo, '2')
        self.assertFalse(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': '310'})
        self.assertEqual(bo, '3')
        self.assertFalse(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': '400'})
        self.assertEqual(bo, '4')
        self.assertTrue(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': '5000'})
        self.assertEqual(bo, False)
        self.assertFalse(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': None})
        self.assertEqual(bo, False)
        self.assertFalse(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': '700'})
        self.assertEqual(bo, '7')
        self.assertTrue(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({'bo': 'U'})
        self.assertEqual(bo, False)
        self.assertFalse(starting)
        bo, starting = BoxScore._get_batting_order_starting_flg({})
        self.assertEqual(bo, False)
        self.assertFalse(starting)


if __name__ == '__main__':
    main()
