import sys,json,operator
from event import ProtestEvent
import narrativeGenerator

"""
Parse the json audit trail json and extract the relevant fields presented in the sample narrative

python parseAuditTrail.py <audit trail json file>

"""

# Sort a dict by value; return a list of (key, value) tuples
def sortDictByValue(eventProbs):
	return sorted(eventProbs.items(), key=operator.itemgetter(1), reverse=True)

def parse(filename):
	file=open(filename)
	data=json.load(file)
	file.close()

	##
	# These all seem pretty stable across different audit trails
	##

	eventProbs=sortDictByValue(data["classification"]["eventType"])

	# footnote 14
	populationProbs=sortDictByValue(data["classification"]["population"])

	# footnote 12
	violenceProbs=sortDictByValue(data["classification"]["violence"])

	# footnote 5
	eventType=data["eventType"]

	# footnote 3
	location=data["location"]
	
	# footnote 2
	date=data["eventDate"]

	# footnote 15
	confidence=data["qs_prediction"]["total"]

	
	event=ProtestEvent(eventType, date, location, eventProbs, populationProbs, violenceProbs, confidence)
	event.printData()

	##
	# These are the fields for the sample narrative, but this will be very different depending on the evidence (e.g., this one happened to be a retweet, so the information presented is specific to that fact)
	##

	# footnote 11
	triggerPhrase=data["derivedFrom"]["triggerPhrase"]
	print "Trigger phrase: %s" % triggerPhrase

	messages=data["derivedFrom"]["derivedMessages"]
	#print messages
	for message in messages:
		submessages=message["derivedFrom"]["derivedMessages"]
		for submessage in submessages:
			# footnote 9
			print submessage["interaction"]["content"]

			#footnote 8
			print submessage["twitter"]["retweeted"]["user"]["screen_name"]

			# footnote 6
			print submessage["twitter"]["retweet"]["created_at"]

			# footnote 7
			print submessage["twitter"]["retweet"]["user"]["screen_name"]

		# footnote 10
		print message["timePhrase"]
	narrativeGenerator.generate(event)
	
	
	

if __name__ == "__main__":
	parse(sys.argv[1])
