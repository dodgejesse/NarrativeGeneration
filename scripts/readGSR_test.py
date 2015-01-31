'''
Example of how to use the GSRReader

python readGSR_test.py ../data/dec.2014.gsr.txt 
'''

import sys
import GSRReader

gsr=GSRReader.readGSR(sys.argv[1])

for country in gsr:
	for year in gsr[country]:
		for month in gsr[country][year]:
			for event in gsr[country][year][month]:
				print "country: %s\tyear: %s\tmonth: %s\tevent:%s" % (country, year, month, event)
