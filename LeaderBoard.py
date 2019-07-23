#!/usr/bin/python

class LeaderBoard(object):
	# may be able to get rid of range
    RANGE = 'A:C'

    def __init__(self, tableInfo, service):
    	# retrieve sheet from google drive and store it
    	'''
    	table format:
    	[['header', 'header', ...], [value, value, value], [value, value, ...],  ...]

    	We transform this into a dictionary
    	{
	     name: {header: value},
	     name: {header: value},...
    	}
    	'''
    	self.tableInfo = tableInfo
    	self.table = {}
    	sheet = service.spreadsheets()
    	result = sheet.values().get(spreadsheetId=tableInfo['id'],
                                range='A:C').execute()
        values = result.get('values', [])
        headers = values[0]

        for row in values[1:]:
        	userName = row[0]
        	self.table[userName] = {}
        	for i, col in enumerate(row[1:], start=1):
        		self.table[userName][headers[i]] = row[i]



    def getTable(self):
    	return self.table

    def getUserData(self, userName):
    	return self.table[userName]

    def updatePointTotal(self, userName, points):
    	self.table[userName]['Points'] += points

    def getLatestRefreshTime(self, userName):
    	return self.table[userName]['latestRefreshTime']

    def updateRemoteLeaderBoard(self):
    	'''
    	Update the sheet in google drive with the new information
    	'''
    	pass



