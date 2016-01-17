#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from bs4 import BeautifulSoup
from unittest import TestCase, main
from pitchpx.game.inning import Inning, AtBat, Pitch
from pitchpx.game.game import Game
from pitchpx.game.players import Players

__author__ = 'Shinichi Nakagawa'


class TestInning(TestCase):

    XML_INNING_HIT = """
<!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt--><hitchart><hip des="Lineout" x="74.54" y="94.54" batter="592518" pitcher="547874" type="O" team="A" inning="1"/><hip des="Groundout" x="161.81" y="160.60" batter="467827" pitcher="547874" type="O" team="A" inning="1"/><hip des="Double" x="211.50" y="111.51" batter="572122" pitcher="592332" type="H" team="H" inning="1"/><hip des="Flyout" x="72.12" y="96.36" batter="448801" pitcher="547874" type="O" team="A" inning="2"/><hip des="Groundout" x="112.11" y="184.84" batter="517370" pitcher="547874" type="O" team="A" inning="2"/><hip des="Lineout" x="149.08" y="162.41" batter="570731" pitcher="547874" type="O" team="A" inning="2"/><hip des="Groundout" x="139.38" y="155.75" batter="452234" pitcher="592332" type="O" team="H" inning="2"/><hip des="Double" x="75.75" y="46.06" batter="457706" pitcher="592332" type="H" team="H" inning="2"/><hip des="Groundout" x="104.24" y="159.99" batter="475247" pitcher="547874" type="O" team="A" inning="3"/><hip des="Flyout" x="177.56" y="140.60" batter="543376" pitcher="547874" type="O" team="A" inning="3"/><hip des="Groundout" x="141.20" y="156.96" batter="518953" pitcher="547874" type="O" team="A" inning="3"/><hip des="Pop Out" x="149.08" y="208.47" batter="491696" pitcher="592332" type="O" team="H" inning="3"/><hip des="Double" x="87.87" y="46.06" batter="429711" pitcher="592332" type="H" team="H" inning="3"/><hip des="Single" x="78.78" y="132.72" batter="429664" pitcher="592332" type="H" team="H" inning="3"/><hip des="Lineout" x="74.54" y="113.33" batter="452234" pitcher="592332" type="O" team="H" inning="3"/><hip des="Groundout" x="156.96" y="155.75" batter="467827" pitcher="547874" type="O" team="A" inning="4"/><hip des="Double" x="64.24" y="56.36" batter="457706" pitcher="592332" type="H" team="H" inning="4"/><hip des="Double" x="53.33" y="136.35" batter="491696" pitcher="592332" type="H" team="H" inning="4"/><hip des="Flyout" x="92.12" y="93.33" batter="606466" pitcher="592332" type="O" team="H" inning="4"/><hip des="Groundout" x="95.75" y="167.87" batter="570731" pitcher="547874" type="O" team="A" inning="5"/><hip des="Groundout" x="143.63" y="156.35" batter="475247" pitcher="547874" type="O" team="A" inning="5"/><hip des="Flyout" x="115.14" y="53.94" batter="543376" pitcher="547874" type="O" team="A" inning="5"/><hip des="Pop Out" x="136.35" y="124.84" batter="429711" pitcher="592332" type="O" team="H" inning="5"/><hip des="Lineout" x="130.29" y="81.21" batter="429664" pitcher="592332" type="O" team="H" inning="5"/><hip des="Lineout" x="143.63" y="67.87" batter="452234" pitcher="592332" type="O" team="H" inning="5"/><hip des="Groundout" x="146.66" y="156.96" batter="518953" pitcher="547874" type="O" team="A" inning="6"/><hip des="Groundout" x="109.08" y="158.78" batter="457706" pitcher="592332" type="O" team="H" inning="6"/><hip des="Lineout" x="66.66" y="97.57" batter="444432" pitcher="592332" type="O" team="H" inning="6"/><hip des="Groundout" x="106.05" y="179.38" batter="543543" pitcher="592332" type="O" team="H" inning="6"/><hip des="Flyout" x="116.36" y="46.66" batter="430945" pitcher="547874" type="O" team="A" inning="7"/><hip des="Groundout" x="144.84" y="152.72" batter="517370" pitcher="547874" type="O" team="A" inning="7"/><hip des="Lineout" x="154.54" y="69.69" batter="491696" pitcher="592332" type="O" team="H" inning="7"/><hip des="Flyout" x="63.63" y="123.63" batter="606466" pitcher="592332" type="O" team="H" inning="7"/><hip des="Groundout" x="143.63" y="150.29" batter="572122" pitcher="592332" type="O" team="H" inning="7"/><hip des="Groundout" x="105.45" y="156.35" batter="543376" pitcher="547874" type="O" team="A" inning="8"/><hip des="Groundout" x="129.69" y="186.05" batter="429664" pitcher="451085" type="O" team="H" inning="8"/><hip des="Lineout" x="96.96" y="113.93" batter="452234" pitcher="451085" type="O" team="H" inning="8"/><hip des="Pop Out" x="83.63" y="182.41" batter="518953" pitcher="547874" type="O" team="A" inning="9"/><hip des="Groundout" x="99.39" y="171.50" batter="592518" pitcher="547874" type="O" team="A" inning="9"/><hip des="Lineout" x="117.57" y="93.93" batter="467827" pitcher="547874" type="O" team="A" inning="9"/></hitchart>
    """

    XML_INNING_01 = """
    <!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt--><inning num="1" away_team="bal" home_team="sea" next="Y"><top><atbat num="1" b="1" s="1" o="1" start_tfs="194021" start_tfs_zulu="2015-08-12T19:40:21Z" batter="592518" stand="R" b_height="6-3" pitcher="547874" p_throws="R" des="Manny Machado lines out to left fielder Brad Miller.  " des_es="Manny Machado batea l&#237;nea de out a jardinero izquierdo Brad Miller.  " event_num="7" event="Lineout" event_es="Línea de Out"  play_guid="7d68f4c6-c7d7-4807-bd1b-99d053c2ce03" home_team_runs="0" away_team_runs="0"><pitch des="Called Strike" des_es="Strike cantado" id="3" type="S" tfs="194050" tfs_zulu="2015-08-12T19:40:50Z" x="121.99" y="186.72" event_num="3" sv_id="150812_124236" play_guid="b207c2f4-b5ca-4e00-97c0-f336763fcf5d" start_speed="86.5" end_speed="79.0" sz_top="3.93" sz_bot="1.77" pfx_x="-7.35" pfx_z="4.41" px="-0.131" pz="1.928" x0="-2.456" y0="50.0" z0="5.365" vx0="8.152" vy0="-126.596" vz0="-3.515" ax="-11.787" ay="28.68" az="-25.033" break_y="23.7" break_angle="21.2" break_length="7.0" pitch_type="SI" type_confidence=".932" zone="8" nasty="51" spin_dir="238.790" spin_rate="1579.341"  cc="" mt=""/><pitch des="Ball" des_es="Bola mala" id="4" type="B" tfs="194130" tfs_zulu="2015-08-12T19:41:30Z" x="85.59" y="202.76" event_num="4" sv_id="150812_124251" play_guid="1aefb106-e51a-4493-b2c8-eb26fd40e40a" start_speed="88.7" end_speed="81.8" sz_top="3.89" sz_bot="1.86" pfx_x="-7.81" pfx_z="4.62" px="0.824" pz="1.334" x0="-2.342" y0="50.0" z0="5.283" vx0="10.698" vy0="-129.607" vz0="-5.365" ax="-13.288" ay="27.16" az="-24.243" break_y="23.8" break_angle="23.8" break_length="6.6" pitch_type="SI" type_confidence=".917" zone="14" nasty="53" spin_dir="239.168" spin_rate="1732.211"  cc="" mt=""/><pitch des="In play, out(s)" des_es="En juego, out(s)" id="5" type="X" tfs="194141" tfs_zulu="2015-08-12T19:41:41Z" x="83.91" y="169.5" event_num="5" sv_id="150812_124306" play_guid="7d68f4c6-c7d7-4807-bd1b-99d053c2ce03" start_speed="81.7" end_speed="75.5" sz_top="3.78" sz_bot="1.77" pfx_x="2.08" pfx_z="-2.45" px="0.868" pz="2.566" x0="-2.41" y0="50.0" z0="5.655" vx0="7.09" vy0="-119.624" vz0="0.281" ax="2.992" ay="24.182" az="-35.636" break_y="23.8" break_angle="-6.8" break_length="10.1" pitch_type="SL" type_confidence=".891" zone="14" nasty="45" spin_dir="40.834" spin_rate="554.940"  cc="" mt=""/></atbat><atbat num="2" b="2" s="1" o="2" start_tfs="194200" start_tfs_zulu="2015-08-12T19:42:00Z" batter="467827" stand="L" b_height="5-11" pitcher="547874" p_throws="R" des="Gerardo Parra grounds out to first baseman Mark Trumbo.  " des_es="Gerardo Parra batea rodado de out a primera base Mark Trumbo.  " event_num="14" event="Groundout" event_es="Roletazo de Out"  play_guid="1e07d7a5-5f1a-4dce-a629-91fbe0b13064" home_team_runs="0" away_team_runs="0"><pitch des="Ball" des_es="Bola mala" id="9" type="B" tfs="194207" tfs_zulu="2015-08-12T19:42:07Z" x="144.44" y="211.19" event_num="9" sv_id="150812_124352" play_guid="64a90d7b-2620-4d06-8590-48ff5010ef2c" start_speed="88.0" end_speed="80.0" sz_top="3.43" sz_bot="1.68" pfx_x="-6.82" pfx_z="6.59" px="-0.72" pz="1.022" x0="-2.639" y0="50.0" z0="5.15" vx0="7.066" vy0="-128.683" vz0="-6.202" ax="-11.231" ay="31.003" az="-21.237" break_y="23.7" break_angle="23.0" break_length="6.1" pitch_type="FF" type_confidence=".886" zone="13" nasty="60" spin_dir="225.759" spin_rate="1767.383"  cc="" mt=""/><pitch des="Ball" des_es="Bola mala" id="10" type="B" tfs="194221" tfs_zulu="2015-08-12T19:42:21Z" x="162.36" y="174.6" event_num="10" sv_id="150812_124406" play_guid="aafadd04-2cdb-4b39-883f-3074e2fe7165" start_speed="80.4" end_speed="73.6" sz_top="3.36" sz_bot="1.64" pfx_x="3.5" pfx_z="0.39" px="-1.19" pz="2.377" x0="-2.659" y0="50.0" z0="5.522" vx0="2.35" vy0="-117.91" vz0="-0.461" ax="4.857" ay="25.365" az="-31.56" break_y="23.8" break_angle="-9.5" break_length="9.4" pitch_type="SL" type_confidence=".914" zone="13" nasty="43" spin_dir="97.205" spin_rate="602.369"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="11" type="S" tfs="194235" tfs_zulu="2015-08-12T19:42:35Z" x="144.83" y="147.66" event_num="11" sv_id="150812_124421" play_guid="b46a93d9-649c-4e8a-b92d-4b9362a59046" start_speed="87.8" end_speed="79.5" sz_top="3.33" sz_bot="1.53" pfx_x="-9.21" pfx_z="4.08" px="-0.73" pz="3.375" x0="-2.543" y0="50.0" z0="5.453" vx0="7.573" vy0="-128.584" vz0="-0.195" ax="-15.142" ay="31.232" az="-25.397" break_y="23.7" break_angle="27.7" break_length="7.1" pitch_type="SI" type_confidence=".919" zone="11" nasty="66" spin_dir="245.888" spin_rate="1871.741"  cc="" mt=""/><pitch des="In play, out(s)" des_es="En juego, out(s)" id="12" type="X" tfs="194301" tfs_zulu="2015-08-12T19:43:01Z" x="117.5" y="195.5" event_num="12" sv_id="150812_124443" play_guid="1e07d7a5-5f1a-4dce-a629-91fbe0b13064" start_speed="82.4" end_speed="75.7" sz_top="3.33" sz_bot="1.53" pfx_x="1.57" pfx_z="-0.07" px="-0.013" pz="1.603" x0="-2.656" y0="50.0" z0="5.423" vx0="5.783" vy0="-120.632" vz0="-2.256" ax="2.284" ay="26.111" az="-32.208" break_y="23.8" break_angle="-5.9" break_length="9.2" pitch_type="SL" type_confidence=".898" zone="8" nasty="28" spin_dir="89.147" spin_rate="274.716"  cc="" mt=""/></atbat><atbat num="3" b="0" s="3" o="3" start_tfs="194330" start_tfs_zulu="2015-08-12T19:43:30Z" batter="430945" stand="R" b_height="6-2" pitcher="547874" p_throws="R" des="Adam Jones strikes out swinging.  " des_es="Adam Jones se poncha tir&#225;ndole.  " event_num="21" event="Strikeout" event_es="Ponche"  play_guid="78070d56-e9ee-417c-a010-9e838c8936a8" home_team_runs="0" away_team_runs="0"><pitch des="Called Strike" des_es="Strike cantado" id="16" type="S" tfs="194344" tfs_zulu="2015-08-12T19:43:44Z" x="103.54" y="149.17" event_num="16" sv_id="150812_124531" play_guid="7f0c7fea-3656-433e-aa65-fff649bc01ea" start_speed="89.6" end_speed="80.9" sz_top="3.66" sz_bot="1.75" pfx_x="-5.84" pfx_z="5.53" px="0.353" pz="3.319" x0="-2.507" y0="50.0" z0="5.383" vx0="9.273" vy0="-131.054" vz0="-0.869" ax="-9.946" ay="33.214" az="-22.685" break_y="23.7" break_angle="18.5" break_length="5.8" pitch_type="FF" type_confidence=".942" zone="3" nasty="58" spin_dir="226.346" spin_rate="1521.744"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="17" type="S" tfs="194400" tfs_zulu="2015-08-12T19:44:00Z" x="161.29" y="177.81" event_num="17" sv_id="150812_124545" play_guid="e576526e-4471-4086-8c9b-48e8112cb90d" start_speed="88.8" end_speed="80.7" sz_top="3.66" sz_bot="1.75" pfx_x="-9.11" pfx_z="2.26" px="-1.162" pz="2.258" x0="-2.538" y0="50.0" z0="5.409" vx0="6.512" vy0="-130.031" vz0="-2.475" ax="-15.316" ay="31.793" az="-28.3" break_y="23.7" break_angle="25.5" break_length="7.8" pitch_type="SI" type_confidence=".920" zone="13" nasty="59" spin_dir="255.805" spin_rate="1762.653"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="18" type="S" tfs="194427" tfs_zulu="2015-08-12T19:44:27Z" x="137.89" y="171.04" event_num="18" sv_id="150812_124613" play_guid="875b6c4b-ccea-4422-9104-d2631a9b3eff" start_speed="84.8" end_speed="77.3" sz_top="3.66" sz_bot="1.75" pfx_x="-9.07" pfx_z="-2.23" px="-0.548" pz="2.509" x0="-2.498" y0="50.0" z0="5.515" vx0="7.606" vy0="-124.164" vz0="-0.024" ax="-13.917" ay="28.764" az="-35.515" break_y="23.7" break_angle="19.0" break_length="10.0" pitch_type="FS" type_confidence=".886" zone="4" nasty="30" spin_dir="283.500" spin_rate="1672.320"  cc="" mt=""/><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="19" type="S" tfs="194455" tfs_zulu="2015-08-12T19:44:55Z" x="83.11" y="140.77" event_num="19" sv_id="150812_124639" play_guid="78070d56-e9ee-417c-a010-9e838c8936a8" start_speed="91.8" end_speed="82.8" sz_top="3.66" sz_bot="1.75" pfx_x="-5.4" pfx_z="5.19" px="0.889" pz="3.63" x0="-2.512" y0="50.0" z0="5.32" vx0="10.762" vy0="-134.16" vz0="-0.081" ax="-9.627" ay="34.901" az="-22.855" break_y="23.7" break_angle="16.7" break_length="5.5" pitch_type="FF" type_confidence=".941" zone="12" nasty="64" spin_dir="225.930" spin_rate="1448.902"  cc="" mt=""/></atbat></top><bottom><atbat num="4" b="3" s="3" o="1" start_tfs="194707" start_tfs_zulu="2015-08-12T19:47:07Z" batter="606466" stand="L" b_height="6-1" pitcher="592332" p_throws="R" des="Ketel Marte strikes out swinging.  " des_es="Ketel Marte se poncha tir&#225;ndole.  " event_num="35" event="Strikeout" event_es="Ponche"  play_guid="dd713571-49b8-4e61-88c1-645cadaa7ec8" home_team_runs="0" away_team_runs="0"><pitch des="Ball" des_es="Bola mala" id="24" type="B" tfs="194738" tfs_zulu="2015-08-12T19:47:38Z" x="183.9" y="176.06" event_num="24" sv_id="150812_124922" play_guid="fec49849-dd44-43e4-899d-3256e799d282" start_speed="87.8" end_speed="79.4" sz_top="3.4" sz_bot="1.57" pfx_x="-4.41" pfx_z="7.87" px="-1.755" pz="2.323" x0="-2.849" y0="50.0" z0="6.076" vx0="4.185" vy0="-128.586" vz0="-5.611" ax="-7.215" ay="32.437" az="-19.226" break_y="23.7" break_angle="16.7" break_length="5.4" pitch_type="FS" type_confidence="2.000" zone="13" nasty="64" spin_dir="209.127" spin_rate="1672.362"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="25" type="S" tfs="194748" tfs_zulu="2015-08-12T19:47:48Z" x="122.64" y="196.63" event_num="25" sv_id="150812_124934" play_guid="b36d96ba-de23-4c3e-b437-2d8927d01a58" start_speed="93.2" end_speed="84.8" sz_top="3.56" sz_bot="1.61" pfx_x="-5.32" pfx_z="8.33" px="-0.148" pz="1.561" x0="-2.486" y0="50.0" z0="5.983" vx0="8.088" vy0="-136.201" vz0="-8.691" ax="-9.842" ay="34.237" az="-16.688" break_y="23.7" break_angle="22.8" break_length="4.5" pitch_type="FF" type_confidence="2.000" zone="13" nasty="40" spin_dir="212.436" spin_rate="1954.480"  cc="" mt=""/><pitch des="Ball" des_es="Bola mala" id="26" type="B" tfs="194805" tfs_zulu="2015-08-12T19:48:05Z" x="170.36" y="187.53" event_num="26" sv_id="150812_124951" play_guid="f28b1f76-28ce-4b54-ada5-74503917dd14" start_speed="92.2" end_speed="84.3" sz_top="3.44" sz_bot="1.57" pfx_x="-7.59" pfx_z="6.55" px="-1.4" pz="1.898" x0="-2.742" y0="50.0" z0="5.973" vx0="6.169" vy0="-134.912" vz0="-7.011" ax="-13.848" ay="32.061" az="-20.152" break_y="23.7" break_angle="29.8" break_length="5.6" pitch_type="FT" type_confidence="2.000" zone="13" nasty="36" spin_dir="229.037" spin_rate="1972.024"  cc="" mt=""/><pitch des="Called Strike" des_es="Strike cantado" id="27" type="S" tfs="194818" tfs_zulu="2015-08-12T19:48:18Z" x="96.49" y="157.08" event_num="27" sv_id="150812_125005" play_guid="cf503f1b-1c83-4c26-89c8-b60c8278cc5c" start_speed="95.4" end_speed="85.8" sz_top="3.4" sz_bot="1.53" pfx_x="-6.14" pfx_z="8.36" px="0.538" pz="3.026" x0="-2.319" y0="50.0" z0="6.014" vx0="9.948" vy0="-139.534" vz0="-5.195" ax="-11.792" ay="39.095" az="-16.046" break_y="23.6" break_angle="27.4" break_length="4.2" pitch_type="FF" type_confidence="2.000" zone="3" nasty="49" spin_dir="216.171" spin_rate="2077.293"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="28" type="S" tfs="194833" tfs_zulu="2015-08-12T19:48:33Z" x="110.63" y="188.37" event_num="28" sv_id="150812_125018" play_guid="26674d40-c2ee-40c6-a22b-b8e6db1b6cfd" start_speed="95.3" end_speed="86.6" sz_top="3.56" sz_bot="1.61" pfx_x="-5.83" pfx_z="7.09" px="0.167" pz="1.867" x0="-2.266" y0="50.0" z0="5.994" vx0="8.708" vy0="-139.322" vz0="-7.908" ax="-11.271" ay="36.107" az="-18.392" break_y="23.7" break_angle="24.0" break_length="4.7" pitch_type="FF" type_confidence=".891" zone="8" nasty="37" spin_dir="219.275" spin_rate="1853.949"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="29" type="S" tfs="194853" tfs_zulu="2015-08-12T19:48:53Z" x="105.07" y="177.52" event_num="29" sv_id="150812_125038" play_guid="063b9cd0-c8c7-4729-820d-0402d10f504d" start_speed="93.5" end_speed="85.5" sz_top="3.56" sz_bot="1.61" pfx_x="-4.32" pfx_z="5.75" px="0.313" pz="2.269" x0="-2.267" y0="50.0" z0="6.0" vx0="8.447" vy0="-136.785" vz0="-6.075" ax="-8.112" ay="32.922" az="-21.303" break_y="23.7" break_angle="15.2" break_length="5.1" pitch_type="FF" type_confidence="2.000" zone="6" nasty="35" spin_dir="216.729" spin_rate="1438.642"  cc="" mt=""/><pitch des="Ball" des_es="Bola mala" id="30" type="B" tfs="194911" tfs_zulu="2015-08-12T19:49:11Z" x="159.62" y="221.5" event_num="30" sv_id="150812_125057" play_guid="ec93692d-3d5f-4eb3-a9fc-f74d5c00216a" start_speed="77.7" end_speed="72.1" sz_top="3.52" sz_bot="1.61" pfx_x="2.19" pfx_z="-5.42" px="-1.118" pz="0.64" x0="-2.63" y0="50.0" z0="6.311" vx0="2.745" vy0="-113.793" vz0="-3.926" ax="2.843" ay="23.183" az="-39.128" break_y="23.8" break_angle="-4.7" break_length="12.5" pitch_type="SL" type_confidence="2.000" zone="13" nasty="41" spin_dir="22.235" spin_rate="957.818"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="31" type="S" tfs="194927" tfs_zulu="2015-08-12T19:49:27Z" x="137.66" y="139.8" event_num="31" sv_id="150812_125114" play_guid="027d5319-ca36-4848-b659-af9f70881dfd" start_speed="94.6" end_speed="85.9" sz_top="3.56" sz_bot="1.61" pfx_x="-5.52" pfx_z="8.81" px="-0.542" pz="3.666" x0="-2.408" y0="50.0" z0="6.183" vx0="7.017" vy0="-138.583" vz0="-4.045" ax="-10.576" ay="35.332" az="-15.221" break_y="23.7" break_angle="28.5" break_length="3.9" pitch_type="FF" type_confidence=".910" zone="11" nasty="54" spin_dir="211.956" spin_rate="2091.790"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="32" type="S" tfs="194951" tfs_zulu="2015-08-12T19:49:51Z" x="124.93" y="150.17" event_num="32" sv_id="150812_125135" play_guid="2f9686eb-2e51-4b5a-9499-32e095b0e82e" start_speed="93.5" end_speed="85.1" sz_top="3.56" sz_bot="1.61" pfx_x="-5.76" pfx_z="8.91" px="-0.208" pz="3.282" x0="-2.354" y0="50.0" z0="6.157" vx0="7.774" vy0="-136.899" vz0="-4.86" ax="-10.778" ay="33.992" az="-15.41" break_y="23.7" break_angle="28.2" break_length="4.1" pitch_type="FF" type_confidence="2.000" zone="2" nasty="38" spin_dir="212.737" spin_rate="2112.054"  cc="" mt=""/><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="33" type="S" tfs="195021" tfs_zulu="2015-08-12T19:50:21Z" x="137.39" y="167.31" event_num="33" sv_id="150812_125158" play_guid="dd713571-49b8-4e61-88c1-645cadaa7ec8" start_speed="94.0" end_speed="85.5" sz_top="3.56" sz_bot="1.61" pfx_x="-3.6" pfx_z="8.86" px="-0.535" pz="2.647" x0="-2.437" y0="50.0" z0="6.004" vx0="6.393" vy0="-137.516" vz0="-6.219" ax="-6.798" ay="34.22" az="-15.364" break_y="23.7" break_angle="17.3" break_length="3.8" pitch_type="FF" type_confidence="2.000" zone="4" nasty="38" spin_dir="202.017" spin_rate="1912.967"  cc="" mt=""/></atbat><atbat num="5" b="0" s="2" o="1" start_tfs="195044" start_tfs_zulu="2015-08-12T19:50:44Z" batter="572122" stand="L" b_height="6-0" pitcher="592332" p_throws="R" des="Kyle Seager doubles (26) on a line drive to right fielder Gerardo Parra.  " des_es="Kyle Seager pega doble (26) con l&#237;nea a jardinero derecho Gerardo Parra.  " event_num="42" event="Double" event_es="Doble"  play_guid="6040a271-f03e-4e9f-8271-1da1d548601d" home_team_runs="0" away_team_runs="0"><pitch des="Called Strike" des_es="Strike cantado" id="37" type="S" tfs="195049" tfs_zulu="2015-08-12T19:50:49Z" x="147.3" y="192.93" event_num="37" sv_id="150812_125236" play_guid="89dd19e9-37eb-41c0-894f-684d81c32870" start_speed="77.7" end_speed="71.6" sz_top="3.35" sz_bot="1.43" pfx_x="2.6" pfx_z="-3.42" px="-0.795" pz="1.698" x0="-2.681" y0="50.0" z0="6.338" vx0="3.464" vy0="-113.936" vz0="-2.206" ax="3.368" ay="23.771" az="-36.529" break_y="23.8" break_angle="-6.1" break_length="11.7" pitch_type="SL" type_confidence="2.000" zone="13" nasty="84" spin_dir="37.716" spin_rate="701.020"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="38" type="S" tfs="195106" tfs_zulu="2015-08-12T19:51:06Z" x="132.25" y="185.81" event_num="38" sv_id="150812_125252" play_guid="3517df0c-b8e2-4dfd-86d4-b17026206cf8" start_speed="95.5" end_speed="86.8" sz_top="3.35" sz_bot="1.43" pfx_x="-5.04" pfx_z="9.72" px="-0.4" pz="1.962" x0="-2.558" y0="50.0" z0="5.909" vx0="7.697" vy0="-139.569" vz0="-8.395" ax="-9.785" ay="35.777" az="-13.215" break_y="23.7" break_angle="27.2" break_length="3.6" pitch_type="FF" type_confidence="2.000" zone="7" nasty="38" spin_dir="207.298" spin_rate="2217.735"  cc="" mt=""/><pitch des="Foul" des_es="Foul" id="39" type="S" tfs="195129" tfs_zulu="2015-08-12T19:51:29Z" x="127.67" y="164.5" event_num="39" sv_id="150812_125314" play_guid="6bc872ae-6be2-402e-ac22-3830c6c1f9ef" start_speed="93.9" end_speed="84.8" sz_top="3.35" sz_bot="1.43" pfx_x="-5.35" pfx_z="10.07" px="-0.28" pz="2.751" x0="-2.577" y0="50.0" z0="6.03" vx0="8.035" vy0="-137.335" vz0="-6.343" ax="-10.002" ay="36.456" az="-13.269" break_y="23.7" break_angle="27.9" break_length="3.7" pitch_type="FF" type_confidence="2.000" zone="1" nasty="35" spin_dir="207.880" spin_rate="2259.371"  cc="" mt=""/><pitch des="In play, no out" des_es="En juego, no out" id="40" type="X" tfs="195157" tfs_zulu="2015-08-12T19:51:57Z" x="145.09" y="181.03" event_num="40" sv_id="150812_125336" play_guid="6040a271-f03e-4e9f-8271-1da1d548601d" start_speed="84.7" end_speed="77.2" sz_top="3.35" sz_bot="1.43" pfx_x="-5.16" pfx_z="4.14" px="-0.737" pz="2.139" x0="-2.661" y0="50.0" z0="6.176" vx0="6.301" vy0="-123.94" vz0="-4.51" ax="-7.897" ay="28.521" az="-25.771" break_y="23.7" break_angle="13.7" break_length="7.3" pitch_type="FS" type_confidence="2.000" zone="13" nasty="41" spin_dir="230.964" spin_rate="1190.061"  cc="" mt=""/><runner id="572122" start="" end="2B" event="Double" event_num="42"/></atbat><atbat num="6" b="0" s="3" o="2" start_tfs="195224" start_tfs_zulu="2015-08-12T19:52:24Z" batter="429711" stand="R" b_height="6-2" pitcher="592332" p_throws="R" des="Franklin Gutierrez strikes out swinging.  " des_es="Franklin Gutierrez se poncha tir&#225;ndole.  " event_num="48" event="Strikeout" event_es="Ponche"  play_guid="5608ca22-aac7-4967-ab78-872d33135650" home_team_runs="0" away_team_runs="0"><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="44" type="S" tfs="195303" tfs_zulu="2015-08-12T19:53:03Z" x="103.43" y="160.51" event_num="44" on_2b="572122" sv_id="150812_125448" play_guid="302e3cdd-36b4-497e-bf17-c8fd7d2c217f" start_speed="97.2" end_speed="87.6" sz_top="3.31" sz_bot="1.44" pfx_x="-6.05" pfx_z="8.75" px="0.356" pz="2.899" x0="-2.272" y0="50.0" z0="6.0" vx0="9.481" vy0="-142.154" vz0="-5.993" ax="-12.098" ay="39.468" az="-14.608" break_y="23.7" break_angle="30.3" break_length="3.8" pitch_type="FF" type_confidence="2.000" zone="3" nasty="57" spin_dir="214.555" spin_rate="2176.775"  cc="" mt=""/><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="45" type="S" tfs="195349" tfs_zulu="2015-08-12T19:53:49Z" x="124.09" y="164.04" event_num="45" on_2b="572122" sv_id="150812_125535" play_guid="9eb0195a-5245-480d-924e-3b25282114eb" start_speed="96.5" end_speed="86.9" sz_top="3.31" sz_bot="1.44" pfx_x="-6.92" pfx_z="9.85" px="-0.186" pz="2.768" x0="-2.401" y0="50.0" z0="5.901" vx0="8.582" vy0="-141.135" vz0="-6.339" ax="-13.629" ay="39.288" az="-12.703" break_y="23.7" break_angle="38.0" break_length="3.8" pitch_type="FF" type_confidence="2.000" zone="2" nasty="32" spin_dir="214.989" spin_rate="2443.102"  cc="" mt=""/><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="46" type="S" tfs="195419" tfs_zulu="2015-08-12T19:54:19Z" x="125.92" y="148.03" event_num="46" on_2b="572122" sv_id="150812_125604" play_guid="5608ca22-aac7-4967-ab78-872d33135650" start_speed="96.8" end_speed="87.2" sz_top="3.31" sz_bot="1.44" pfx_x="-6.5" pfx_z="10.53" px="-0.234" pz="3.361" x0="-2.082" y0="50.0" z0="6.1" vx0="7.448" vy0="-141.689" vz0="-5.566" ax="-12.901" ay="39.404" az="-11.201" break_y="23.7" break_angle="40.4" break_length="3.4" pitch_type="FF" type_confidence="2.000" zone="11" nasty="45" spin_dir="211.595" spin_rate="2521.220"  cc="" mt=""/></atbat><atbat num="7" b="1" s="3" o="3" start_tfs="195446" start_tfs_zulu="2015-08-12T19:54:46Z" batter="429664" stand="L" b_height="6-0" pitcher="592332" p_throws="R" des="Robinson Cano strikes out swinging.  " des_es="Robinson Cano se poncha tir&#225;ndole.  " event_num="56" event="Strikeout" event_es="Ponche"  play_guid="374385c4-0034-4ffc-a493-82259695fae9" home_team_runs="0" away_team_runs="0"><po des="Pickoff Attempt 2B" event_num="50" /><pitch des="Ball In Dirt" des_es="Bola por el suelo" id="51" type="B" tfs="195534" tfs_zulu="2015-08-12T19:55:34Z" x="93.21" y="223.82" event_num="51" on_2b="572122" sv_id="150812_125719" play_guid="bd186d9b-4456-4c94-ac39-99ebda92eacb" start_speed="86.9" end_speed="79.9" sz_top="3.75" sz_bot="1.71" pfx_x="-8.09" pfx_z="2.92" px="0.624" pz="0.554" x0="-2.63" y0="50.0" z0="5.87" vx0="10.73" vy0="-126.81" vz0="-7.766" ax="-13.043" ay="28.207" az="-27.387" break_y="23.8" break_angle="20.5" break_length="7.8" pitch_type="FS" type_confidence="2.000" zone="14" nasty="82" spin_dir="249.846" spin_rate="1589.524"  cc="" mt=""/><pitch des="Called Strike" des_es="Strike cantado" id="52" type="S" tfs="195610" tfs_zulu="2015-08-12T19:56:10Z" x="132.63" y="182.27" event_num="52" on_2b="572122" sv_id="150812_125755" play_guid="e81ec651-fba0-4778-8c2c-e9b0c8c211b4" start_speed="96.7" end_speed="87.1" sz_top="3.75" sz_bot="1.71" pfx_x="-4.55" pfx_z="8.68" px="-0.41" pz="2.093" x0="-2.248" y0="50.0" z0="5.949" vx0="6.705" vy0="-141.417" vz0="-7.947" ax="-8.982" ay="39.743" az="-14.963" break_y="23.7" break_angle="22.6" break_length="3.8" pitch_type="FF" type_confidence="2.000" zone="7" nasty="42" spin_dir="207.558" spin_rate="1991.639"  cc="" mt=""/><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="53" type="S" tfs="195642" tfs_zulu="2015-08-12T19:56:42Z" x="103.2" y="159.05" event_num="53" on_2b="572122" sv_id="150812_125821" play_guid="2936a996-9068-444a-9121-643e77ce2224" start_speed="97.0" end_speed="87.2" sz_top="3.75" sz_bot="1.71" pfx_x="-4.75" pfx_z="8.18" px="0.362" pz="2.953" x0="-2.212" y0="50.0" z0="5.992" vx0="8.834" vy0="-141.848" vz0="-5.553" ax="-9.434" ay="40.345" az="-15.867" break_y="23.6" break_angle="21.8" break_length="3.9" pitch_type="FF" type_confidence="2.000" zone="6" nasty="35" spin_dir="210.049" spin_rate="1926.830"  cc="" mt=""/><pitch des="Swinging Strike" des_es="Strike tir&#225;ndole" id="54" type="S" tfs="195708" tfs_zulu="2015-08-12T19:57:08Z" x="105.45" y="157.83" event_num="54" on_2b="572122" sv_id="150812_125853" play_guid="374385c4-0034-4ffc-a493-82259695fae9" start_speed="98.5" end_speed="88.5" sz_top="3.75" sz_bot="1.71" pfx_x="-5.1" pfx_z="6.95" px="0.303" pz="2.998" x0="-2.266" y0="50.0" z0="6.012" vx0="9.078" vy0="-144.064" vz0="-5.293" ax="-10.422" ay="42.019" az="-17.89" break_y="23.6" break_angle="22.0" break_length="4.2" pitch_type="FF" type_confidence="2.000" zone="6" nasty="34" spin_dir="216.114" spin_rate="1780.641"  cc="" mt=""/><runner id="572122" start="2B" end="" event="Pickoff Attempt 2B" event_num="56"/></atbat></bottom></inning>
    """
    XML_GAME = """
<!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt--><game type="R" local_game_time="12:40" game_pk="415346" game_time_et="03:40 PM" gameday_sw="P">
	<team type="home" code="sea" file_code="sea" abbrev="SEA" id="136" name="Seattle" name_full="Seattle Mariners" name_brief="Mariners" w="54" l="61" division_id="200" league_id="103" league="AL"/>
	<team type="away" code="bal" file_code="bal" abbrev="BAL" id="110" name="Baltimore" name_full="Baltimore Orioles" name_brief="Orioles" w="57" l="56" division_id="201" league_id="103" league="AL"/>
	<stadium id="680" name="Safeco Field" venue_w_chan_loc="USWA0395" location="Seattle, WA"/>
</game>
    """
    XML_PLAYERS = """
<!--Copyright 2015 MLB Advanced Media, L.P.  Use of any content on this page acknowledges agreement to the terms posted here http://gdx.mlb.com/components/copyright.txt--><game venue="Safeco Field" date="August 12, 2015">
	<team type="away" id="BAL" name="Baltimore Orioles">
		<player id="429666" first="J.J." last="Hardy" num="2" boxname="Hardy, J" rl="R" bats="R" position="SS" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".233" hr="7" rbi="30"/>
		<player id="430945" first="Adam" last="Jones" num="10" boxname="Jones, A" rl="R" bats="R" position="CF" current_position="CF" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="3" game_position="CF" avg=".280" hr="19" rbi="56"/>
		<player id="434622" first="Ubaldo" last="Jimenez" num="31" boxname="Jimenez, U" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".200" hr="0" rbi="1" wins="9" losses="7" era="3.79"/>
		<player id="446308" first="Matt" last="Wieters" num="32" boxname="Wieters" rl="R" bats="S" position="C" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".278" hr="5" rbi="17"/>
		<player id="448801" first="Chris" last="Davis" num="19" boxname="Davis, C" rl="R" bats="L" position="1B" current_position="1B" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="4" game_position="1B" avg=".254" hr="31" rbi="83"/>
		<player id="451085" first="Brian" last="Matusz" num="17" boxname="Matusz" rl="L" bats="L" position="P" current_position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="1" losses="2" era="2.52"/>
		<player id="456068" first="Miguel" last="Gonzalez" num="50" boxname="Gonzalez, Mi" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="9" losses="8" era="4.45"/>
		<player id="456665" first="Steve" last="Pearce" num="28" boxname="Pearce" rl="R" bats="R" position="LF" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".227" hr="7" rbi="24"/>
		<player id="460099" first="Nolan" last="Reimold" num="14" boxname="Reimold" rl="R" bats="R" position="LF" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".226" hr="2" rbi="8"/>
		<player id="467827" first="Gerardo" last="Parra" num="18" boxname="Parra, G" rl="L" bats="L" position="LF" current_position="RF" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="2" game_position="RF" avg=".315" hr="10" rbi="32"/>
		<player id="475054" first="Chaz" last="Roe" num="65" boxname="Roe" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="2" losses="2" era="3.12"/>
		<player id="475247" first="Ryan" last="Flaherty" num="3" boxname="Flaherty" rl="R" bats="L" position="2B" current_position="SS" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="7" game_position="SS" avg=".212" hr="4" rbi="22"/>
		<player id="501957" first="Chris" last="Tillman" num="30" boxname="Tillman" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="8" losses="7" era="4.66"/>
		<player id="502154" first="Zach" last="Britton" num="53" boxname="Britton" rl="L" bats="L" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="2" losses="0" era="1.57"/>
		<player id="503285" first="Darren" last="O'Day" num="56" boxname="O'Day" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="5" losses="1" era="1.25"/>
		<player id="516809" first="Junior" last="Lake" num="48" boxname="Lake" rl="R" bats="R" position="RF" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".212" hr="1" rbi="5"/>
		<player id="517370" first="Jimmy" last="Paredes" num="38" boxname="Paredes" rl="R" bats="S" position="D" current_position="DH" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="5" game_position="DH" avg=".276" hr="10" rbi="41"/>
		<player id="518953" first="David" last="Lough" num="9" boxname="Lough" rl="L" bats="L" position="LF" current_position="LF" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="9" game_position="LF" avg=".206" hr="4" rbi="12"/>
		<player id="519008" first="T.J." last="McFarland" num="66" boxname="McFarland" rl="L" bats="L" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="0" losses="2" era="2.37"/>
		<player id="542960" first="Brad" last="Brach" num="35" boxname="Brach" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="4" losses="2" era="2.60"/>
		<player id="543376" first="Caleb" last="Joseph" num="36" boxname="Joseph, C" rl="R" bats="R" position="C" current_position="C" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="8" game_position="C" avg=".252" hr="10" rbi="38"/>
		<player id="570731" first="Jonathan" last="Schoop" num="6" boxname="Schoop" rl="R" bats="R" position="2B" current_position="2B" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="6" game_position="2B" avg=".302" hr="8" rbi="22"/>
		<player id="571710" first="Mychal" last="Givens" num="60" boxname="Givens" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="1" losses="0" era="0.00"/>
		<player id="592329" first="Jason" last="Garcia" num="61" boxname="Garcia, Ja" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="5.52"/>
		<player id="592332" first="Kevin" last="Gausman" num="39" boxname="Gausman" rl="R" bats="L" position="P" current_position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="0" game_position="P" avg=".000" hr="0" rbi="0" wins="2" losses="3" era="4.56"/>
		<player id="592518" first="Manny" last="Machado" num="13" boxname="Machado, M" rl="R" bats="R" position="3B" current_position="3B" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" bat_order="1" game_position="3B" avg=".300" hr="24" rbi="57"/>
		<player id="592869" first="Tyler" last="Wilson" num="63" boxname="Wilson, T" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="2" losses="1" era="2.19"/>
		<player id="605541" first="Mike" last="Wright" num="59" boxname="Wright, M" rl="R" bats="R" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".500" hr="0" rbi="0" wins="2" losses="3" era="4.99"/>
		<player id="612672" first="Wei-Yin" last="Chen" num="16" boxname="Chen" rl="L" bats="L" position="P" status="A" team_abbrev="BAL" team_id="110" parent_team_abbrev="BAL" parent_team_id="110" avg=".000" hr="0" rbi="0" wins="6" losses="6" era="3.21"/>
<coach position="manager" first="Buck" last="Showalter" id="427469" num="26"/><coach position="hitting_coach" first="Scott" last="Coolbaugh" id="112635" num="47"/><coach position="assistant_hitting_coach" first="Einar" last="Diaz" id="113330" num="55"/><coach position="pitching_coach" first="Dave" last="Wallace" id="123855" num="37"/><coach position="first_base_coach" first="Wayne" last="Kirby" id="117114" num="24"/><coach position="third_base_coach" first="Bobby" last="Dickerson" id="433638" num="11"/><coach position="bench_coach" first="John" last="Russell" id="121571" num="77"/><coach position="bullpen_coach" first="Dom" last="Chiti" id="492826" num="54"/>	</team>
	<team type="home" id="SEA" name="Seattle Mariners">
		<player id="346847" first="Joe" last="Beimel" num="97" boxname="Beimel" rl="L" bats="L" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="2" losses="1" era="3.16"/>
		<player id="407845" first="Fernando" last="Rodney" num="56" boxname="Rodney" rl="R" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="5" losses="4" era="5.21"/>
		<player id="429664" first="Robinson" last="Cano" num="22" boxname="Cano" rl="R" bats="L" position="2B" current_position="2B" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="4" game_position="2B" avg=".268" hr="12" rbi="50"/>
		<player id="429711" first="Franklin" last="Gutierrez" num="30" boxname="Gutierrez, F" rl="R" bats="R" position="LF" current_position="DH" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="3" game_position="DH" avg=".306" hr="5" rbi="13"/>
		<player id="433587" first="Felix" last="Hernandez" num="34" boxname="Hernandez, F" rl="R" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="14" losses="6" era="3.11"/>
		<player id="443558" first="Nelson" last="Cruz" num="23" boxname="Cruz, N" rl="R" bats="R" position="RF" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".324" hr="34" rbi="70"/>
		<player id="444432" first="Mark" last="Trumbo" num="35" boxname="Trumbo" rl="R" bats="R" position="RF" current_position="1B" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="7" game_position="1B" avg=".249" hr="14" rbi="42"/>
		<player id="452234" first="Seth" last="Smith" num="7" boxname="Smith, S" rl="L" bats="L" position="LF" current_position="RF" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="5" game_position="RF" avg=".256" hr="9" rbi="29"/>
		<player id="452666" first="Tom" last="Wilhelmsen" num="54" boxname="Wilhelmsen" rl="R" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="1" losses="2" era="4.28"/>
		<player id="457706" first="Austin" last="Jackson" num="16" boxname="Jackson, A" rl="R" bats="R" position="CF" current_position="CF" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="6" game_position="CF" avg=".249" hr="6" rbi="30"/>
		<player id="489149" first="Logan" last="Morrison" num="20" boxname="Morrison" rl="L" bats="L" position="1B" current_position="1B" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".220" hr="12" rbi="36"/>
		<player id="491696" first="Jesus" last="Sucre" num="2" boxname="Sucre" rl="R" bats="R" position="C" current_position="C" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="9" game_position="C" avg=".091" hr="1" rbi="1"/>
		<player id="515052" first="Mayckol" last="Guaipe" num="53" boxname="Guaipe" rl="R" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="0" losses="3" era="6.97"/>
		<player id="518703" first="Charlie" last="Furbush" num="41" boxname="Furbush" rl="L" bats="L" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="1" losses="1" era="2.08"/>
		<player id="519169" first="Rob" last="Rasmussen" num="50" boxname="Rasmussen" rl="L" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="1" losses="1" era="13.50"/>
		<player id="524968" first="Jesus" last="Montero" num="63" boxname="Montero, J" rl="R" bats="R" position="1B" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".289" hr="2" rbi="9"/>
		<player id="543543" first="Brad" last="Miller" num="5" boxname="Miller, B" rl="R" bats="L" position="SS" current_position="LF" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="8" game_position="LF" avg=".253" hr="9" rbi="36"/>
		<player id="543557" first="Mike" last="Montgomery" num="37" boxname="Montgomery" rl="L" bats="L" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="4" losses="4" era="3.25"/>
		<player id="543716" first="David" last="Rollins" num="59" boxname="Rollins, D" rl="L" bats="L" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="0" losses="0" era="7.82"/>
		<player id="547874" first="Hisashi" last="Iwakuma" num="18" boxname="Iwakuma" rl="R" bats="R" position="P" current_position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="0" game_position="P" avg=".000" hr="0" rbi="0" wins="3" losses="2" era="4.41"/>
		<player id="572020" first="James" last="Paxton" num="65" boxname="Paxton" rl="L" bats="L" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="3" losses="3" era="3.70"/>
		<player id="572122" first="Kyle" last="Seager" num="15" boxname="Seager, K" rl="R" bats="L" position="3B" current_position="3B" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="2" game_position="3B" avg=".263" hr="16" rbi="45"/>
		<player id="572287" first="Mike" last="Zunino" num="3" boxname="Zunino" rl="R" bats="R" position="C" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".168" hr="10" rbi="26"/>
		<player id="573064" first="Vidal" last="Nuno" num="38" boxname="Nuno" rl="L" bats="L" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".143" hr="0" rbi="1" wins="0" losses="2" era="2.64"/>
		<player id="592836" first="Taijuan" last="Walker" num="32" boxname="Walker, T" rl="R" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".111" hr="0" rbi="1" wins="8" losses="7" era="4.60"/>
		<player id="605476" first="Carson" last="Smith" num="39" boxname="Smith, Ca" rl="R" bats="R" position="P" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" avg=".000" hr="0" rbi="0" wins="1" losses="5" era="2.66"/>
		<player id="606466" first="Ketel" last="Marte" num="4" boxname="Marte, K" rl="R" bats="S" position="SS" current_position="SS" status="A" team_abbrev="SEA" team_id="136" parent_team_abbrev="SEA" parent_team_id="136" bat_order="1" game_position="SS" avg=".235" hr="0" rbi="1"/>
<coach position="manager" first="Lloyd" last="McClendon" id="118576" num="21"/><coach position="hitting_coach" first="Edgar" last="Martinez" id="118365" num="11"/><coach position="pitching_coach" first="Rick" last="Waits" id="123796" num="47"/><coach position="first_base_coach" first="Chris" last="Woodward" id="218595" num="28"/><coach position="third_base_coach" first="Rich" last="Donnelly" id="427123" num="26"/><coach position="bench_coach" first="Trent" last="Jewett" id="492495" num="45"/><coach position="bullpen_coach" first="Mike" last="Rojas" id="492527" num="48"/><coach position="quality_control_coach" first="Chris" last="Prieto" id="408076" num="88"/><coach position="bullpen_catcher" first="Jason" last="Phillips" id="282993" num="62"/><coach position="coach" first="Andy" last="Van Slyke" id="123653" num="43"/>	</team>
<umpires><umpire position="home" name="Jeff Nelson" id="427362" first="Jeff" last="Nelson"/><umpire position="first" name="Laz Diaz" id="427113" first="Laz" last="Diaz"/><umpire position="second" name="Chris Guccione" id="427197" first="Chris" last="Guccione"/><umpire position="third" name="Cory Blaser" id="484183" first="Cory" last="Blaser"/></umpires></game>
    """
    XML_ATBAT_DATASET = """
<atbat num="5" b="0" s="2" o="1" start_tfs="195044" start_tfs_zulu="2015-08-12T19:50:44Z" batter="572122" stand="L" b_height="6-0" pitcher="592332" p_throws="R" des="Kyle Seager doubles (26) on a line drive to right fielder Gerardo Parra. " des_es="Kyle Seager pega doble (26) con línea a jardinero derecho Gerardo Parra. " event_num="42" event="Double" event_es="Doble" play_guid="6040a271-f03e-4e9f-8271-1da1d548601d" home_team_runs="0" away_team_runs="0">
<pitch des="Called Strike" des_es="Strike cantado" id="37" type="S" tfs="195049" tfs_zulu="2015-08-12T19:50:49Z" x="147.3" y="192.93" event_num="37" sv_id="150812_125236" play_guid="89dd19e9-37eb-41c0-894f-684d81c32870" start_speed="77.7" end_speed="71.6" sz_top="3.35" sz_bot="1.43" pfx_x="2.6" pfx_z="-3.42" px="-0.795" pz="1.698" x0="-2.681" y0="50.0" z0="6.338" vx0="3.464" vy0="-113.936" vz0="-2.206" ax="3.368" ay="23.771" az="-36.529" break_y="23.8" break_angle="-6.1" break_length="11.7" pitch_type="SL" type_confidence="2.000" zone="13" nasty="84" spin_dir="37.716" spin_rate="701.020" cc="" mt=""/>
<pitch des="Foul" des_es="Foul" id="38" type="S" tfs="195106" tfs_zulu="2015-08-12T19:51:06Z" x="132.25" y="185.81" event_num="38" sv_id="150812_125252" play_guid="3517df0c-b8e2-4dfd-86d4-b17026206cf8" start_speed="95.5" end_speed="86.8" sz_top="3.35" sz_bot="1.43" pfx_x="-5.04" pfx_z="9.72" px="-0.4" pz="1.962" x0="-2.558" y0="50.0" z0="5.909" vx0="7.697" vy0="-139.569" vz0="-8.395" ax="-9.785" ay="35.777" az="-13.215" break_y="23.7" break_angle="27.2" break_length="3.6" pitch_type="FF" type_confidence="2.000" zone="7" nasty="38" spin_dir="207.298" spin_rate="2217.735" cc="" mt=""/>
<pitch des="Foul" des_es="Foul" id="39" type="S" tfs="195129" tfs_zulu="2015-08-12T19:51:29Z" x="127.67" y="164.5" event_num="39" sv_id="150812_125314" play_guid="6bc872ae-6be2-402e-ac22-3830c6c1f9ef" start_speed="93.9" end_speed="84.8" sz_top="3.35" sz_bot="1.43" pfx_x="-5.35" pfx_z="10.07" px="-0.28" pz="2.751" x0="-2.577" y0="50.0" z0="6.03" vx0="8.035" vy0="-137.335" vz0="-6.343" ax="-10.002" ay="36.456" az="-13.269" break_y="23.7" break_angle="27.9" break_length="3.7" pitch_type="FF" type_confidence="2.000" zone="1" nasty="35" spin_dir="207.880" spin_rate="2259.371" cc="" mt=""/>
<pitch des="In play, no out" des_es="En juego, no out" id="40" type="X" tfs="195157" tfs_zulu="2015-08-12T19:51:57Z" x="145.09" y="181.03" event_num="40" sv_id="150812_125336" play_guid="6040a271-f03e-4e9f-8271-1da1d548601d" start_speed="84.7" end_speed="77.2" sz_top="3.35" sz_bot="1.43" pfx_x="-5.16" pfx_z="4.14" px="-0.737" pz="2.139" x0="-2.661" y0="50.0" z0="6.176" vx0="6.301" vy0="-123.94" vz0="-4.51" ax="-7.897" ay="28.521" az="-25.771" break_y="23.7" break_angle="13.7" break_length="7.3" pitch_type="FS" type_confidence="2.000" zone="13" nasty="41" spin_dir="230.964" spin_rate="1190.061" cc="" mt=""/>
<runner id="572122" start="" end="2B" event="Double" event_num="42"/>
</atbat>
    """
    XML_PITCH = """
<pitch des="In play, no out" des_es="En juego, no out" id="40" type="X" tfs="195157" tfs_zulu="2015-08-12T19:51:57Z" x="145.09" y="181.03" event_num="40" sv_id="150812_125336" play_guid="6040a271-f03e-4e9f-8271-1da1d548601d" start_speed="84.7" end_speed="77.2" sz_top="3.35" sz_bot="1.43" pfx_x="-5.16" pfx_z="4.14" px="-0.737" pz="2.139" x0="-2.661" y0="50.0" z0="6.176" vx0="6.301" vy0="-123.94" vz0="-4.51" ax="-7.897" ay="28.521" az="-25.771" break_y="23.7" break_angle="13.7" break_length="7.3" pitch_type="FS" type_confidence="2.000" zone="13" nasty="41" spin_dir="230.964" spin_rate="1190.061" cc="" mt=""/>
    """

    def setUp(self):
        self.hit_location = Inning._read_hit_chart_data(BeautifulSoup(TestInning.XML_INNING_HIT, 'lxml'))
        self.inning_01 = BeautifulSoup(TestInning.XML_INNING_01, 'lxml')
        self.game = Game._generate_game_object(
            BeautifulSoup(TestInning.XML_GAME, 'lxml'),
            dt.strptime('2015-08-12', '%Y-%m-%d'),
            1
        )
        self.players = Players._read_objects(BeautifulSoup(TestInning.XML_PLAYERS, 'lxml'), self.game)
        self.innings = Inning(self.game, self.players)

    def tearDown(self):
        pass

    def test_inning_events_top(self):
        """
        Inning events(top)
        """
        self.innings._inning_events(self.inning_01.find('top'), 1, Inning.INNINGS['top'], self.hit_location)
        self.assertEqual(len(self.innings.atbats), 3)
        self.assertEqual(len(self.innings.pitches), 11)

    def test_inning_events_bottom(self):
        """
        Inning events(top)
        """
        self.innings._inning_events(self.inning_01.find('bottom'), 1, Inning.INNINGS['bottom'], self.hit_location)
        self.assertEqual(len(self.innings.atbats), 4)
        self.assertEqual(len(self.innings.pitches), 21)

    def test_atbat_pa(self):
        """
        atbat dataset(PA)
        """
        ab = AtBat.pa(
            BeautifulSoup(TestInning.XML_ATBAT_DATASET, 'lxml').find('atbat'),
            self.game,
            self.players.rosters,
            1,
            1,
            1,
            self.hit_location
        )
        self.assertEqual(ab['retro_game_id'], 'SEA201508120')
        self.assertEqual(ab['year'], 2015)
        self.assertEqual(ab['month'], 8)
        self.assertEqual(ab['day'], 12)
        self.assertEqual(ab['st_fl'], 'F')
        self.assertEqual(ab['regseason_fl'], 'T')
        self.assertEqual(ab['playoff_fl'], 'F')
        self.assertEqual(ab['game_type'], 'R')
        self.assertEqual(ab['game_type_des'], 'Regular Season')
        self.assertEqual(ab['local_game_time'], '12:40')
        self.assertEqual(ab['game_id'], '415346')
        self.assertEqual(ab['home_team_id'], 'sea')
        self.assertEqual(ab['away_team_id'], 'bal')
        self.assertEqual(ab['home_team_lg'], 'AL')
        self.assertEqual(ab['away_team_lg'], 'AL')
        self.assertEqual(ab['interleague_fl'], 'F')
        self.assertEqual(ab['park_id'], '680')
        self.assertEqual(ab['park_name'], 'Safeco Field')
        self.assertEqual(ab['park_location'], 'Seattle, WA')
        self.assertEqual(ab['inning_number'], 1)
        self.assertEqual(ab['bat_home_id'], 1)
        self.assertEqual(ab['outs_ct'], 1)
        self.assertEqual(ab['pit_mlbid'], '592332')
        self.assertEqual(ab['pit_first_name'], 'Kevin')
        self.assertEqual(ab['pit_last_name'], 'Gausman')
        self.assertEqual(ab['pit_box_name'], 'Gausman')
        self.assertEqual(ab['pit_hand_cd'], 'R')
        self.assertEqual(ab['bat_mlbid'], '572122')
        self.assertEqual(ab['bat_first_name'], 'Kyle')
        self.assertEqual(ab['bat_last_name'], 'Seager')
        self.assertEqual(ab['bat_box_name'], 'Seager, K')
        self.assertEqual(ab['bat_hand_cd'], 'L')
        self.assertEqual(ab['ab_number'], 5)
        self.assertEqual(ab['start_bases'], '___')
        self.assertEqual(ab['end_bases'], '_2_')
        self.assertEqual(ab['event_outs_ct'], 1)
        self.assertEqual(ab['ab_des'], 'Kyle Seager doubles (26) on a line drive to right fielder Gerardo Parra. ')
        self.assertEqual(ab['event_tx'], 'Double')
        self.assertEqual(ab['event_cd'], 21)
        self.assertEqual(ab['hit_x'], 211.50)
        self.assertEqual(ab['hit_y'], 111.51)

    def test_atbat_result(self):
        """
        atbat dataset(Result)
        """
        soup = BeautifulSoup(TestInning.XML_ATBAT_DATASET, 'lxml').find('atbat')
        pa = AtBat.pa(
            soup,
            self.game,
            self.players.rosters,
            1,
            1,
            1,
            self.hit_location
        )
        pitches = self.innings._get_pitch(soup,pa)
        ab = AtBat.result(soup, pa, pitches)
        self.assertEqual(ab['ball_ct'], 0)
        self.assertEqual(ab['strike_ct'], 2)
        self.assertEqual(ab['pitch_seq'], 'SSSX')
        self.assertEqual(ab['pitch_type_seq'], 'SL|FF|FF|FS')
        self.assertEqual(ab['battedball_cd'], 'L')

    def test_pitch(self):
        """
        pitch dataset(Result)
        """
        soup = BeautifulSoup(TestInning.XML_ATBAT_DATASET, 'lxml').find('atbat')
        pa = AtBat.pa(
            soup,
            self.game,
            self.players.rosters,
            1,
            1,
            1,
            self.hit_location
        )
        pitch = Pitch.row(
            BeautifulSoup(TestInning.XML_PITCH, 'lxml').find('pitch'),
            pa,
            self.innings._get_pitch(soup, pa)[0:3],
            0,
            0,
        )
        self.assertEqual(pitch['retro_game_id'], 'SEA201508120')
        self.assertEqual(pitch['year'], 2015)
        self.assertEqual(pitch['month'], 8)
        self.assertEqual(pitch['day'], 12)
        self.assertEqual(pitch['st_fl'], 'F')
        self.assertEqual(pitch['regseason_fl'], 'T')
        self.assertEqual(pitch['playoff_fl'], 'F')
        self.assertEqual(pitch['game_type'], 'R')
        self.assertEqual(pitch['game_type_des'], 'Regular Season')
        self.assertEqual(pitch['local_game_time'], '12:40')
        self.assertEqual(pitch['game_id'], '415346')
        self.assertEqual(pitch['home_team_id'], 'sea')
        self.assertEqual(pitch['away_team_id'], 'bal')
        self.assertEqual(pitch['home_team_lg'], 'AL')
        self.assertEqual(pitch['away_team_lg'], 'AL')
        self.assertEqual(pitch['interleague_fl'], 'F')
        self.assertEqual(pitch['park_id'], '680')
        self.assertEqual(pitch['park_name'], 'Safeco Field')
        self.assertEqual(pitch['park_location'], 'Seattle, WA')
        self.assertEqual(pitch['inning_number'], 1)
        self.assertEqual(pitch['bat_home_id'], 1)
        self.assertEqual(pitch['outs_ct'], 1)
        self.assertEqual(pitch['pit_mlbid'], '592332')
        self.assertEqual(pitch['pit_first_name'], 'Kevin')
        self.assertEqual(pitch['pit_last_name'], 'Gausman')
        self.assertEqual(pitch['pit_box_name'], 'Gausman')
        self.assertEqual(pitch['pit_hand_cd'], 'R')
        self.assertEqual(pitch['bat_mlbid'], '572122')
        self.assertEqual(pitch['bat_first_name'], 'Kyle')
        self.assertEqual(pitch['bat_last_name'], 'Seager')
        self.assertEqual(pitch['bat_box_name'], 'Seager, K')
        self.assertEqual(pitch['bat_hand_cd'], 'L')
        self.assertEqual(pitch['ab_number'], 5)
        self.assertEqual(pitch['start_bases'], '___')
        self.assertEqual(pitch['end_bases'], '_2_')
        self.assertEqual(pitch['event_outs_ct'], 1)
        self.assertEqual(pitch['pa_ball_ct'], 0)
        self.assertEqual(pitch['pa_strike_ct'], 0)
        self.assertEqual(pitch['pitch_seq'], 'SSSX')
        self.assertEqual(pitch['pa_terminal_fl'], 'T')
        self.assertEqual(pitch['pa_event_cd'], 21)
        self.assertEqual(pitch['pitch_res'], 'X')
        self.assertEqual(pitch['pitch_des'], 'In play, no out')
        self.assertEqual(pitch['pitch_id'], 40)
        self.assertEqual(pitch['x'], 145.09)
        self.assertEqual(pitch['y'], 181.03)
        self.assertEqual(pitch['start_speed'], 84.7)
        self.assertEqual(pitch['end_speed'], 77.2)
        self.assertEqual(pitch['sz_top'], 3.35)
        self.assertEqual(pitch['sz_bot'], 1.43)
        self.assertEqual(pitch['pfx_x'], -5.16)
        self.assertEqual(pitch['pfx_z'], 4.14)
        self.assertEqual(pitch['px'], -0.737)
        self.assertEqual(pitch['pz'], 2.139)
        self.assertEqual(pitch['x0'], -2.661)
        self.assertEqual(pitch['y0'], 50.0)
        self.assertEqual(pitch['z0'], 6.176)
        self.assertEqual(pitch['vx0'], 6.301)
        self.assertEqual(pitch['vy0'], -123.94)
        self.assertEqual(pitch['vz0'], -4.51)
        self.assertEqual(pitch['ax'], -7.897)
        self.assertEqual(pitch['ay'], 28.521)
        self.assertEqual(pitch['az'], -25.771)
        self.assertEqual(pitch['break_y'], 23.7)
        self.assertEqual(pitch['break_angle'], 13.7)
        self.assertEqual(pitch['break_length'], 7.3)
        self.assertEqual(pitch['pitch_type'], 'FS')
        self.assertEqual(pitch['pitch_type_seq'], 'SL|FF|FF|FS')
        self.assertEqual(pitch['type_confidence'], 2.0)
        self.assertEqual(pitch['zone'], 13)
        self.assertEqual(pitch['spin_dir'], 230.964)
        self.assertEqual(pitch['spin_rate'], 1190.061)
        self.assertEqual(pitch['sv_id'], '150812_125336')

if __name__ == '__main__':
    main()
