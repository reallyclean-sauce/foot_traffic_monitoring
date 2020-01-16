#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:15:11 2020

@author: jericolinux
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

import auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_CREDENTIALS = 'credentials.json'

authInst = auth.auth(SCOPES, CLIENT_CREDENTIALS)
credentials = authInst.get_credentials()
drive_service = build('drive', 'v3', credentials=credentials)


def listfiles(size):
    # Call the Drive v3 API
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            
def listfolders():
    folderlist = []
    page_token = None
    while True:
        response = drive_service.files().list(q="name='temp' and mimeType='application/vnd.google-apps.folder'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
#        if page_token is None:
        break

        
#    return folderlist


def uploadfile(filename, filepath, folder_id, mimetype):
    file_metadata = {
            'name': filename,
            'parents': [folder_id]
            }
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    
def createfolder(foldername, folder_id):
    file_metadata = {
        'name': foldername, 
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))
    
    return file.get('id')




if __name__ == '__main__':
    filename = 'cifar10.png'
    filepath = './cifar10.png'
    img_mime = 'image/png'
    #uploadfile(filename, filepath, 'image/png')
    #
#    folder_id = createfolder('temp')
    #uploadfile(filename, filepath, folder_id, img_mime)
    
    #listfolders()