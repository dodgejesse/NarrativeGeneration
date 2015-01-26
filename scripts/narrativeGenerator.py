import sys
from event import ProtestEvent

def generate(event):
    printCriticalInsight(event)
    printPerformanceAssessment(event)

def printPerformanceAssessment(event):
    print 'Based on past events in this area, this event has a',
    (violence, score) = event.getMax(event.violenceProbs)[0]
    print `score` + ' chance of being',
    if violence == '2':
        print 'violent.'
    else:
        print 'nonviolent.'
    print 'Based on past events in this area, there is a ' + protestTypeAboveThreshold(event)

def protestTypeAboveThreshold(event):
    eventProbs = event.getMaxAboveThreshold(event.eventProbs, .25)
    
    print 
    print 
    print event.getMax(event.eventProbs)
    print event.getMaxAboveThreshold(event.eventProbs, .1)
    print
    print
    stringEventProbs = eventProbs[0][1] + ' probability that this event is related to ' + convertEventNumIntoDescriptivePhrase(eventNum)

    # to loop over the other events that are above threshold
    for (eventNum, prob) in eventProbs:
        stringEventProbs = stringEventProbs + ', and a ' + prob + ' that this event is related to ' + convertEventNumIntoDescriptivePhrase(eventNum)
    stringEventProbs = stringEventProbs + '.'
        
    

def printCriticalInsight(event):
    print 'Our algorithm forecasts there will be a',
    if event.getMax(event.violenceProbs)[0][0] == '2': 
        print 'violent',
    else:
        print 'nonviolent',
    print 'protest on ' + formatDate(event.date) + ' in ' + event.location[2] + ', ' + event.location[0] + '.',
    print 'We predict the protest will involve' + phraseForPopulation(event) + '. The protest will be related to',
    print protestTypeMax(event)
    
    print
    


# returns the one max scoring type of protest
def protestTypeMax(event):
    maxScoringEventType = event.getMax(event.eventProbs)
    typePhrase = 'discontent about ' + convertEventNumIntoDescriptivePhrase(maxScoringEventType[0][0])
    # to loop over the events that tied for first
    for i in range(len(maxScoringEventType) - 1):
        (eventNum, prob) = maxScoringEventType[i]
        typePhrase = typePhrase + ' or ' + convertEventNumIntoDescriptivePhrase(eventNum)
    return typePhrase

# this returns a desciptive phrase for a given event num. 
# we don't know what the descriptive phrases all are yet, so this is incomplete.
def convertEventNumIntoDescriptivePhrase(eventNum):
    if eventNum == '013':
        return ' discontent about energy and resources'
    else:
        return ' event type ' + eventNum

# makes phrases like "membes of the general public" or "the pubilc
def phraseForPopulation(event):
    maxScoringPops = event.getMax(event.populationProbs)
    populationPhrase = ''
    for (population, score) in maxScoringPops:
        if population == 'General Population':
            populationPhrase = populationPhrase + ' members of the general population'
        elif population == 'Religious':
            populationPhrase = populationPhrase +' members of religious groups'
        elif population == 'Refugees/Displaced':
            populationPhrase = populationPhrase +' refugees or displaced people'
        elif population == 'Media':
            populationPhrase = populationPhrase +' the media'
        else:
            populationPhrase = populationPhrase + ' ' + populationPhrase.lower() + ' people'
    return populationPhrase

# formats the date string from, e.g., 2014-12-13T00:00:00 to December 13th, 2014.
def formatDate(date):
    year = date[0:4]
    # to convert the month number to the month name:
    month = date[5:7]
    monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthName = monthNames[int(month) - 1]
    day = date[8:10]
    dayName = ''
    if day == '01':
        dayName = '1st'
    elif day == '02':
        dayName = '2nd'
    elif day == '03':
        dayName = '3rd'
    elif day == '21':
        dayName = '21st'
    elif day == '22':
        dayName = '22nd'
    elif day == '23':
        dayName = '23rd'
    elif day == '31':
        dayName = '31st'
    else:
        dayNum = int(day)
        dayName = `dayNum` + 'th'
    return monthName + ' ' + dayName + ', ' + year

