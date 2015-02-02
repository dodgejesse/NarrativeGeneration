import sys
from event import ProtestEvent

def generate(event):
    printCriticalInsight(event)
    printVerbalizedAuditTrail(event)
    printPerformanceAssessment(event)

def printVerbalizedAuditTrail(event):
    if event.source == 'RSS':
        printRSSSource(event)
    elif event.source == 'twitter-url':
        printTwitterURL(event)
    elif event.source == 'twitter-public':
        printTwitterPublic(event)
    else:
        print "PROBLEM WITH FINDING SOURCE!!"
        sys.exit(0)

def printRSSSource(event):
    print 'This warning was generated based on a news article.',
    print 'The trigger phrase "' + event.triggerPhrase + '" was used to determine that an event will happen.'

def printTwitterURL(event):
    print 'This warning was generated base on a tweet.'
    print 'the trigger phrase "' + event.triggerPhrase + '" was used to determine that an event will happen.'

def printTwitterPublic(event):
    print 'This warning was generated based on a tweet.'
    print 'the trigger phrase "' + event.triggerPhrase + '" was used to determine that an event will happen.'

def printPerformanceAssessment(event):
    print 'Based on past events in this area, this event has a',
    (violence, score) = event.getMax(event.violenceProbs)[0]
    print `round(score, 2)` + ' chance of being',
    if violence == '2':
        print 'violent.'
    else:
        print 'nonviolent.'
    print 'Based on past events in this area, there is a ' + protestTypeAboveThreshold(event)
    print 'We expect this event to involve ' + protestPopulationAboveThreshold(event)
    print 'Overall, we are ' + getConfidence(event) + ' in this prediction.'

def getConfidence(event):
    if event.confidence > 3:
        return 'confident'
    else:
        return 'not confident'

def protestPopulationAboveThreshold(event):
    populationProbs = event.getMaxAboveThreshold(event.populationProbs, .1)
    stringPopProbs = getPopulationName(populationProbs[0][0]) + ' with probability ' + `round(populationProbs[0][1], 2)`

    # to loop over the other events that are above threshold
    
    for i in range(len(populationProbs)-1):
        (population, prob) = populationProbs[i + 1]
        stringPopProbs = stringPopProbs + ', and' + getPopulationName(population) + ' with probability ' + `round(prob, 2)`
    stringPopProbs = stringPopProbs + '.'
    return stringPopProbs


def protestTypeAboveThreshold(event):
    eventProbs = event.getMaxAboveThreshold(event.eventProbs, .1)
    stringEventProbs = `round(eventProbs[0][1], 2)` + ' probability that this event is related to ' + convertEventNumIntoDescriptivePhrase(eventProbs[0][0])

    # to loop over the other events that are above threshold
    
    for i in range(len(eventProbs)-1):
        (eventNum, prob) = eventProbs[i + 1]
        stringEventProbs = stringEventProbs + ', and a ' + `round(prob, 2)` + ' probability that this event is related to ' + convertEventNumIntoDescriptivePhrase(eventNum)
    stringEventProbs = stringEventProbs + '.'
    return stringEventProbs
        
    

def printCriticalInsight(event):
    print 'Our algorithm forecasts there will be a',
    if event.getMax(event.violenceProbs)[0][0] == '2': 
        print 'violent',
    else:
        print 'nonviolent',
    print 'protest on ' + formatDate(event.date) + ' in ' + event.location[2] + ', ' + event.location[0] + '.',
    print 'We predict the protest will involve' + populationMax(event) + '. The protest will be related to',
    print protestTypeMax(event) + '.'
    
    print

# returns the one max scoring type of protest
def protestTypeMax(event):
    maxScoringEventType = event.getMax(event.eventProbs)
    typePhrase = 'discontent about ' + convertEventNumIntoDescriptivePhrase(maxScoringEventType[0][0])
    # to loop over the events that tied for first
    for i in range(len(maxScoringEventType) - 1):
        (eventNum, prob) = maxScoringEventType[i + 1]
        typePhrase = typePhrase + ' or ' + convertEventNumIntoDescriptivePhrase(eventNum)
    return typePhrase

# this returns a desciptive phrase for a given event num. 
def convertEventNumIntoDescriptivePhrase(eventNum):
    stringBuilder = ''
    if eventNum == '011':
        stringBuilder += 'employment and wages'
    elif eventNum == '012':
        stringBuilder += 'housing'
    elif eventNum == '013':
        stringBuilder += 'energy'
    elif eventNum == '014':
        stringBuilder += 'resources'
    elif eventNum == '015':
        stringBuilder += 'economic policies'
    elif eventNum == '016':
        stringBuilder += 'government policies'
    else:
        print "PROBLEM WHEN DEALING WITH EVENT CODES!"
    return stringBuilder


# makes phrases like "membes of the general public" or "the pubilc
def populationMax(event):
    maxScoringPops = event.getMax(event.populationProbs)
    popPhrase = getPopulationName(maxScoringPops[0][0])
    # to loop over the events that tied for first
    for i in range(len(maxScoringPops) - 1):
        (population, prob) = maxScoringPops[i + 1]
        popPhrase = popPhrase + ' or ' + getPopulationName(population)
    return popPhrase

def getPopulationName(population):
    populationPhrase = ''
    if population == 'General Population':
        populationPhrase = populationPhrase + ' members of the general population'
    elif population == 'Religious':
        populationPhrase = populationPhrase +' members of religious groups'
    elif population == 'Refugees/Displaced':
        populationPhrase = populationPhrase +' refugees or displaced people'
    elif population == 'Media':
        populationPhrase = populationPhrase +' the media'
    else:
        populationPhrase = populationPhrase + ' ' + population.lower() + ' people'
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

