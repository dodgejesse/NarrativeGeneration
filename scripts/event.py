"""
Class to store data for protest events
"""

class ProtestEvent:

	# All of these args seem required for any event prediction
	def __init__(self, eventType, date, location, eventProbs, populationProbs, violenceProbs, confidence):
		self.date=date
		self.eventType=eventType
		self.date=date
		self.location=location
		self.confidence=confidence

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
		for i in range(1,len(array)):
			(k,v)=array[i]
			if v > threshold:
				plist.append((k,v))

	# prints the data in this event
	def printData(self):
		print "Event type: %s" % self.eventType
		print "Date: %s" % self.date
		print "Location: %s" % self.location
		print "Confidence: %s" % self.confidence
		print "Event: %s" % (self.getMax(self.eventProbs))
		print "Population: %s" % (self.getMaxAboveThreshold(self.populationProbs, .25))
		print "Violence: %s" % (self.getMax(self.violenceProbs))
