"""
Class to store data for protest events
"""

import re

class ProtestEvent:

	# All of these args seem required for any event prediction
	def __init__(self, eventType, date, location, eventProbs, populationProbs, violenceProbs, confidence, location_popln_size, source, triggerPhrase, comments):
		self.date=date
		self.eventType=eventType
		self.date=date
		self.location=location
		self.confidence=confidence
		self.location_popln_size=location_popln_size
		self.retweets=-1

		self.comments=comments

		matcher=re.search("retweet_cnt: (\d+)$", comments)
		if matcher != None:
			self.retweets=int(matcher.group(1))
		
		self.tweet = ''
		matcher=re.search("tweet:(.*) phrase:", comments)
		if matcher != None:
			self.tweet=matcher.group(1)
		
		self.url = ''
		matcher=re.search("url:(.*) phrase:", comments)
		if matcher != None:
			self.url=matcher.group(1)
		


		# print "SOURCE: %s" % source
		# print "TWEET: %s" % tweet
		# print "PHRASE: %s" % phrase
		# print "RETWEETS: %s" % retweets

		# twitter-public, twitter-url, RSS
		self.source=source

		self.triggerPhrase=triggerPhrase

		##
		# all probability distributions; keep all in case we want to discuss uncertainty (or if the max doesn't win by much)
		##

		# all event probabilities
		self.eventProbs=eventProbs
		# all population probabilities
		self.populationProbs=populationProbs
		# all violence probabilities
		self.violenceProbs=violenceProbs
		
	# pop max value of (k,v) list; or multiple if ties
	def getMax(self, array):
		plist=[]
		(maxPop, maxProb)=array[0]
		plist.append((maxPop, maxProb))
		for i in range(1,len(array)):
			(k,v)=array[i]
			if v == maxProb:
				plist.append((k,v))

		return plist

	# pop max values of (k,v) list if v > threshold
	def getMaxAboveThreshold(self, array, threshold):
		plist=[]
		for i in range(0,len(array)):
			(k,v)=array[i]
			if float(v) > threshold:
				plist.append((k,v))
		return plist

	# prints the data in this event
	def printData(self):
		print "Event type: %s" % self.eventType
		print "Date: %s" % self.date
		print "Location: %s" % self.location
		print "Confidence: %s" % self.confidence
		print "Event: %s" % (self.getMax(self.eventProbs))
		print "Population: %s" % (self.getMaxAboveThreshold(self.populationProbs, .25))
		print "Violence: %s" % (self.getMax(self.violenceProbs))
		print "Source: %s" % self.source
