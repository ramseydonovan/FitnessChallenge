#!/usr/bin/python

class GoogleSheet(object):
	# may be able to get rid of range
    RANGE = 'A:C'

    def __init__(self, sheetInfo):
    	# need to decide how we are going to determine the username
    	# maybe the file name? Maybe make a subfolder for everyone, FitnessChallengeDonovan
    	sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetInfo['id'],
                                range=RANGE).execute()
        values = result.get('values', [])
        self.values = values
        self.sheetInfo = sheetInfo