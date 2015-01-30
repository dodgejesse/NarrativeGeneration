from gsrEvent import GSREvent
from dateutil.parser import parse

def readGSR(filename):

	gsr={}

	targetEvents=set()
	for i in range(1,8):
		targetEvents.add("01%s" % i)
		targetEvents.add("01%s1" % i)
		targetEvents.add("01%s2" % i)
			
	file=open(filename)
	# skip header
	file.readline()
	for line in file:
		cols=line.rstrip().split("\t")
		if len(cols) > 10:
			eid=cols[0]
			country=cols[4]
			state=cols[5]
			city=cols[6]
			event=cols[7]
			population=cols[8]
			date=parse(cols[9])

			if event not in targetEvents:
				continue

			event=GSREvent(eid, country, state, city, event, population, date)

			if country not in gsr:
				gsr[country]={}

			if date.year not in gsr[country]:
				gsr[country][date.year]={}
			if date.month not in gsr[country][date.year]:
				gsr[country][date.year][date.month]=[]

			gsr[country][date.year][date.month].append(event)

	file.close()

	return gsr

