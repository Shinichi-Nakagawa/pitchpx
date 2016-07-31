#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import click
from pitchpx.mlbam import MlbAm, MlbAmBadParameter

__author__ = 'Shinichi Nakagawa'


@click.command()
@click.option('--start', '-s', required=True, help='Start Day(YYYYMMDD)')
@click.option('--end', '-e', required=True, help='End Day(YYYYMMDD)')
@click.option('--out', '-o', required=True, default='.', help='Output directory(default:".")')
@click.option(
    '--client_secret_file', '-c', required=False, help='Upload to Google Drive(input to client_secret.json file Path)'
)
def main(start, end, out, client_secret_file):
    """
    Scrape a MLBAM Data
    :param start: Start Day(YYYYMMDD)
    :param end: End Day(YYYYMMDD)
    :param out: Output directory(default:"../output/mlb")
    """
    try:
        logging.basicConfig(level=logging.WARNING)
        MlbAm.scrape(start, end, out, client_secret_file)
    except MlbAmBadParameter as e:
        raise click.BadParameter(e)
