#!/usr/bin/python
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import LeaderBoard
import GoogleSheet
import User
import fitness_utils

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'

FITNESS_SHEET_ID = '1RDEQkUp3NJvemEYEm83LgDuRXRTX08L2Dy0nu16PPyQ'
SAMPLE_RANGE_NAME = 'A:C'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # list files in google drive
    print('google drive')
    service2 = build('drive', 'v3', credentials=creds)
    results = service2.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, parents, capabilities)").execute()
    items = results.get('files', [])

    FitnessChallengeFolderID = ''
    if not items:
        print('No files found.')
    else:
        for item in items:
            if (item['name'] == 'FitnessChallenge'):
            	FitnessChallengeFolderID = item['id']

    leaderBoardInfo = {}
    userFolders = []
    userFiles = []
    if FitnessChallengeFolderID:
    	# get all file id's in FitnessChallenge directory
        for item in items:
            parents = item.get('parents')
            if parents and (FitnessChallengeFolderID in parents):
                if (item['name'] == 'LeaderBoard'):
    				# save the LeaderBoard sheet to update later
                    leaderBoardInfo = item
                elif item['capabilities']['canListChildren']:
                	# if this is a directory then it is a user's folder
                	userFolders.append(item)
                else:
    			    userFiles.append(item)

    # build a map of user folders to its sub files
    directoryStructureMap = {}
    for userFolder in userFolders:
    	directoryStructureMap[userFolder['id']] = {'self': userFolder, 'children': []}

    for userFile in userFiles:
    	for parent in userFile['parents']:
    	    if parent in directoryStructureMap.keys():
    		    directoryStructureMap[parent]['children'].append(userFile)
    		    break

    # create service for sheets
    service = build('sheets', 'v4', credentials=creds)

    # Generate the leader board
    try:
        leaderBoard = LeaderBoard.LeaderBoard(leaderBoardInfo, service)
    except Exception as e:
    	print('Error when retrieving the leader board')
    	raise

    # get the spread sheet for each new file
    users = []
    for userFolderID in directoryStructureMap.keys():
    	userFolder = directoryStructureMap[userFolderID]
    	# create the user
    	user = User.User(userFolder['self'])
    	# create this user's GoogleSheet objects
        for userFile in userFolder['children']:
            googleSheet = GoogleSheet.GoogleSheet(userFile, values)
            user.addChildSheet(googleSheet)
        users.append(user)

    # Now we have a list of users with their child sheets
    for user in users:
    	print (user.getName())

    # perform calculations and then update the leader board




if __name__ == '__main__':
    main()

