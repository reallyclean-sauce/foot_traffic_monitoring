#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:01:39 2020

@author: jericolinux

This gets the credentials required for accessing the
google drive APIs
"""
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# CLIENT_CREDENTIALS = 'client_id.json'

class auth:
    """
    For authentication
    """

    def __init__(self, SCOPES, CLIENT_CREDENTIALS):
        self.SCOPES = SCOPES
        self.CLIENT_CREDENTIALS = CLIENT_CREDENTIALS
        # print(CLIENT_CREDENTIALS)


    def get_credentials(self):
        """
        Returns credentials for the project
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_CREDENTIALS, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds
