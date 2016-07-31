#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os
import argparse


from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as CredentialStorage
from oauth2client.tools import run_flow as run_oauth2
from oauth2client import tools

__author__ = 'Shinichi Nakagawa'


class GoogleClient(object):
    """
    Google API Client base class
    """

    SERVICE_NAME = None
    VERSIONS = None
    FLAGS = argparse.ArgumentParser(parents=[tools.argparser]).parse_args(args=[])

    def __init__(self, client_secret_file, settings):
        """
        Google API Client
        :param client_secret_file: client_secret.json
        :param settings: settings params(dict)
        """
        self.client_secret_file = client_secret_file
        self.settings = settings
        self.service = self.get_service()

    def get_service(self):
        """
        Get API Service
        :return: service client
        """
        credential_storage = CredentialStorage(
            os.path.join(self.settings['credential_dir'], self.settings['credential_file'])
        )
        credentials = credential_storage.get()
        if credentials is None or credentials.invalid:
            flow = flow_from_clientsecrets(
                self.client_secret_file,
                scope=self.settings['scopes']
            )
            flow.user_agent = self.settings['app_name']
            credentials = run_oauth2(flow, credential_storage, flags=self.FLAGS)
        http = credentials.authorize(httplib2.Http())
        return build(self.SERVICE_NAME, self.VERSIONS, http=http)


class GoogleDrive(GoogleClient):
    """
    Google Storage API
    """

    SERVICE_NAME = 'storage'
    VERSIONS = 'v1'
