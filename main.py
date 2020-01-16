#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:45:15 2020

@author: jericolinux
"""

import os
import cv2
import sys
from access_gdrive import uploadfile, createfolder


# Prerequisite Codes:
with open('prerequisite.txt', 'r') as f:
    x = f.read()  
    # Prerequisite is not satisfied
    if x == '0':
        # Installation prerequisite
        print("Install anaconda first")
        print("Use the environment specified: 'environment.yml'")
        print("Use this command: 'conda env create -f environment.yml'")
        
        # Change credentials for data@upcapes.org
        print("Prerequisite is not yet satisfied!")
        print("Have you changed the credentials.json for data@upcapes.org?")
        print("'1' or '0'")
        ans = input("Answer: ")
        if ans == '0':
            # print("")
            sys.exit('Change it first!')
            
        # Next prerequisite
        print("We will first create a new folder in your current gdrive")
        print("using the credentials.json that is within this folder")
        print("Copy the folder ID that will be shown")
        print("Then, change the 'folder_id' in the code in 'main.py'")
        createfolder('extracted_data', '')
        
        print("Have you changed it?")
        print("'1' or '0'")
        ans = input("Answer: ")
        if ans == '1':
            with open('prerequisite.txt', 'w') as f:
                f.write('1')
            sys.exit("Rerun the program. Don't mind the error")
        else:
            sys.exit('Copy it First!')
            sys.exit('Then, rerun the program.')
            
        
        


mimetype_dict = {
        'folder': 'application/vnd.google-apps.folder',
        'image' : 'image/jpeg'
        }

# Get all current folder names
DIR = './extracted_data'
shift_list = [name for name in os.listdir(DIR)]

# Get input from user for end of recording time
while True:
    print("Input the starting time of your shift.")
    print("Video should be in the same format.")
    print("Save the video into the 'data' folder.")
    print("Format: {hr}_{min}_{am/pm}")
    
    starting_shift_time = input("Starting Shift Time: ")
    # starting_shift_time = "10_30_am"
    if starting_shift_time not in shift_list:
        break
    else: 
        print("Shift exists!")

print("Starting shift time indicated: {}".format(starting_shift_time))

# Get an input video file
filepath = './data/{}.avi'.format(starting_shift_time)

    
# Prepare for uploading the files
# Folder Name in Gdrive is extracted_data
# Prototype folder: 'temp'; folder_id = 1kP9VaFmYI-dM9kM0ctVAbhyuJjh6RrdU
folder_id = '1kP9VaFmYI-dM9kM0ctVAbhyuJjh6RrdU' # This needs to be replaced

newlyCreatedFolderID = createfolder(starting_shift_time, folder_id)

# Read the video
vidcap = cv2.VideoCapture(filepath)
success,image = vidcap.read()

# Get the FPS
fps = vidcap.get(cv2.CAP_PROP_FPS)
print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

# Split video into video frames
# Save each frame into a folder
folder_path = "./extracted_data/{}".format(starting_shift_time)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Loop to extract the frames
count = 0
sec = 8
while success:
    if not count % (fps*sec):  
        # Save the frame locally
        img_name = "frame{}.jpg".format(str(count))
        im_path = folder_path + '/' + img_name
        cv2.imwrite(im_path, image)     # save frame as JPEG file   
        print('Read a new frame: ', success)
        
        # Upload the frame
        uploadfile(img_name, im_path, newlyCreatedFolderID, mimetype_dict['image'])

    success,image = vidcap.read() # Optimize this
    count += 1  
    




















