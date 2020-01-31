#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:45:15 2020

@author: jericolinux

This program gets saved videos in src_dir
and extract frames from it and save it to dest_dir
then upload the frames to google drive using folder_id
"""

import os
import cv2
import sys
from access_gdrive import uploadfile, createfolder

# Global Variables

# Prepare for uploading the files
# Folder Name in Gdrive is extracted_data
# Prototype folder: 'temp'; folder_id = 1kP9VaFmYI-dM9kM0ctVAbhyuJjh6RrdU
folder_id = '1FRr_uzBeg2vmSNPlAKy9spnFuu64f8ex' # The folder ID of the dest_data
src_dir = 'data' # The dir of the source video files
dest_dir = 'extracted_data' # The dir of the extracted frames

mimetype_dict = {
        'folder': 'application/vnd.google-apps.folder',
        'image' : 'image/jpeg'
        }

# Get all currently extracted videos
DIR = f'./{dest_dir}'
saved_data = [name for name in os.listdir(DIR)]

# Get input from user for end of recording time
while True:
    print("Input the venue, the floor, and the starting time of your shift.")
    print("Video should be in the same format.")
    print("Save the video into the 'data' folder.")
    print("Format: {venue}_{floor}_{hr}_{min}_{am/pm}")
    print("all in small caps")

    new_data = input("Input: ")
    if new_data not in saved_data:
        break
    else:
        print("Input already exists!")

# new_data = "ice_first_10_30_am" # Debugging Variable
print(f'Starting shift time indicated: {new_data}')

# Get an input video file
filepath = f'./{src_dir}/{new_data}.avi'
newlyCreatedFolderID = createfolder(new_data, folder_id, 1)

# Read the video
try:
    vidcap = cv2.VideoCapture(filepath)
    success,image = vidcap.read()
except:
    raise SystemExit("File does not exist!")

# Get the FPS
fps = vidcap.get(cv2.CAP_PROP_FPS)
print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

# Split video into video frames
# Save each frame into a folder
folder_path = f'./{parent_dir}/{new_data}'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Loop to extract the frames
count = 0
sec = 10
while success:
    if not count % (fps*sec):
        # Save the frame locally
        img_name = f'frame{str(count)}.jpg'
        im_path = folder_path + '/' + img_name
        cv2.imwrite(im_path, image)     # save frame as JPEG file
        print('Read a new frame: ', success)

        # Upload the frame
        uploadfile(img_name, im_path, newlyCreatedFolderID, mimetype_dict['image'])

    success,image = vidcap.read() # Optimize this
    count += 1
