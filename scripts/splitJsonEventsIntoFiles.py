import sys,json,os

# read in a big json file (with multiple events) and write them out to their own individual files.
# creates the folder if it does not exist yet.
def read(filename, folder):

	if not os.path.exists(folder):
		os.makedirs(folder)
	
	page=""
	file=open(filename)
	for line in file:
		page+=line
	file.close()

	events=json.loads(page)

	for event in events:
		jsonEvent=json.loads(event)
		embersId=jsonEvent["embersId"]

		print "writing %s" % embersId
		outfile="%s/%s" % (folder, embersId)
		with open(outfile, 'w') as out:
			json.dump(jsonEvent, out)

# arg1 = big input file (with multiple events)
# arg2 = output directory to write the individual event files into.  
# event names will be their associated embersId (from the json file)

# Usage: python splitJsonEventsIntoFiles.py ../data/planned_protests_2014-11-01_2015-01-13.json ../data/split_events
read(sys.argv[1], sys.argv[2])