#!/usr/bin/python

class User(object):
	# may be able to get rid of range
    RANGE = 'A:C'

    def __init__(self, userInfo):
    	# need to decide how we are going to determine the username
    	# maybe the file name? Maybe make a subfolder for everyone, FitnessChallengeDonovan
    	self.name = userInfo['name']
    	self.info = userInfo
    	self.children = []

    def addChildSheet(self, sheet):
    	self.children.append(sheet)

    def getName(self):
    	return self.name