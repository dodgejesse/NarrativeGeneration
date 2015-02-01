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

	classdata=json.loads(data['classification'])

	eventProbs=sortDictByValue(classdata["eventType"])

	# footnote 14
	populationProbs=sortDictByValue(classdata["population"])

	# footnote 12
	violenceProbs=sortDictByValue(classdata["violence"])

	# footnote 5
	eventType=data["eventType"]

	# footnote 3
	location=data["location"]

	location_popln_size=long(data["location_popln_size"])
	
	# footnote 2
	date=data["eventDate"]

	derivedFrom=json.loads(data["derivedFrom"])
	source=derivedFrom["source"]
	triggerPhrase=derivedFrom["triggerPhrase"]

	# comments are an unstructured mess; might be good to get it to us more structured.
	comments=derivedFrom["comments"]

	# footnote 15
	confidence=json.loads(data["qs_prediction"])["total"]

	
	event=ProtestEvent(eventType, date, location, eventProbs, populationProbs, violenceProbs, confidence, location_popln_size, source, triggerPhrase, comments)

	narrativeGenerator.generate(event)
	
	
	

if __name__ == "__main__":
	parse(sys.argv[1])
