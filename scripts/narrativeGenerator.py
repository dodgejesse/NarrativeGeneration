import sys
from event import ProtestEvent
from dateutil.parser import parse


maxProb = .34

def generate(event, gsr):
    print '\n\n\n'
    printCriticalInsight(event)
    printComparativeStatements(event, gsr)
    printVerbalizedAuditTrail(event)
    printPerformanceAssessment(event)
    print '\n\n\n'

def printComparativeStatements(event, gsr):
    print 'Context: Statements comparing this event to other events across time and in different locations.'
    print
    printDurationSinceLastProtestOfThisGroup(event, gsr)
    print
    print

def printDurationSinceLastProtestOfThisGroup(event, gsr):
    maxDate = parse(event.date)
    mostRecentDate = ''
    
    for year in gsr[event.location[0]]:
        givenYear = gsr[event.location[0]][year]
        for month in givenYear:
            givenMonth = givenYear[month]
            for gsrEvent in givenMonth:
                if eventsSameTypeSamePlace(event, gsrEvent):
                    if firstDateBeforeSecond(mostRecentDate, gsrEvent.date, maxDate):
                        mostRecentDate = gsrEvent.date
    
    print 'The most recent time a',
    if event.eventType[3] == '1':
        print 'nonviolent',
    else:
        print 'violent',
    print 'protest related to', convertEventNumIntoDescriptivePhrase(event.eventType[0:3]),
    print 'happened here was', printDateDifference(maxDate, mostRecentDate)

def eventsSameTypeSamePlace(event, gsrEvent):
    #return event.eventType == gsrEvent.event and unicode(event.location[0], 'utf8') == unicode(gsrEvent.country, 'utf8') and unicode(event.location[1], 'utf8') == unicode(gsrEvent.state, 'utf8') and unicode(event.location[2], 'utf8') == unicode(gsrEvent.city, 'utf8')
    return event.eventType == gsrEvent.event and event.location[0] == unicode(gsrEvent.country, 'utf8') and event.location[1] == unicode(gsrEvent.state, 'utf8') and event.location[2] == unicode(gsrEvent.city, 'utf8')

def printDateDifference(curEvent, prevEvent):


    if prevEvent == '':
        return 'never.'
    elif curEvent.year == prevEvent.year and curEvent.month == prevEvent.month and curEvent.day - 1 == prevEvent.day:
        return 'the day before the predicted event.'
    elif curEvent.year == prevEvent.year and curEvent.month == prevEvent.month and curEvent.day > prevEvent.day:
        return `curEvent.day - prevEvent.day` + ' days before the predicted event.'
    elif curEvent.year == prevEvent.year and curEvent.month - 1 == prevEvent.month:
        return 'a month before the predicted event.'
    elif curEvent.year == prevEvent.year and curEvent.month > prevEvent.month:
        return `curEvent.month - prevEvent.month` + ' months before the predicted event.'
    elif curEvent.year - 1 == prevEvent.year:
        return 'the year before the predicted event.'
    elif curEvent.year > prevEvent.year:
        return `curEvent.year - prevEvent.year` + ' years before the predicted event.'
    else:
        return 'never.'

def firstDateBeforeSecond(curMaxDate, newDate, maxDate):
    # cases: stored = '' => true
    # stored > new => return false
    # stored < new && new < maxDate => return true
    if curMaxDate == '':
        return True
    elif (curMaxDate.year > newDate.year or (curMaxDate.year == newDate.year and curMaxDate.month > newDate.month) or (curMaxDate.year == newDate.year and curMaxDate.month == newDate.month and curMaxDate.day >= newDate.day)):
        return False
    else:
        return not (newDate.year > maxDate.year or (newDate.year == maxDate.year and newDate.month > maxDate.month) or (newDate.year == maxDate.year and newDate.month == maxDate.month and newDate.day >= maxDate.day))

def printVerbalizedAuditTrail(event):
    print 'Verbalized audit trail: Description of the sources of information used in generating this warning.'
    print
    if event.source == 'RSS':
        printRSSSource(event)
    elif event.source == 'twitter-url':
        printTwitterURL(event)
    elif event.source == 'twitter-public':
        printTwitterPublic(event)
    else:
        print "PROBLEM WITH FINDING SOURCE!!"
        sys.exit(0)
    print
    print

def printRSSSource(event):
    if event.url != '':
        print 'This warning was generated based on a news article at the following URL: ' + event.url
    else:
        print 'This warning was generated based on a news article.'
    print 'The trigger phrase "' + event.triggerPhrase + '" was found in the news article, and used to predict that an event will happen.'

def printTwitterURL(event):
    if event.url != '':
        print 'This warning was generated based on a tweet at the following URL: ' + event.url
    else:
        print 'This warning was generated based on a tweet.'
    print 'the trigger phrase "' + event.triggerPhrase + '" was found in the tweet, and used to predict that an event will happen.'

def printTwitterPublic(event):
    if event.tweet != '':
        print 'This warning was generated based on the following tweet: "' + event.tweet + '"'
    else:
        print 'This warning was generated based on a tweet.'
    if event.retweets != -1:
        print 'This tweet was retweeted ' + `event.retweets` + ' times.'
    print 'The trigger phrase "' + event.triggerPhrase + '" was found in the tweet, and used to predict that an event will happen.'

def printPerformanceAssessment(event):
    print 'Performance Assessment: How confident we are in the predictions within this warning.'
    print
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
    if event.confidence > 3.5:
        return 'extremely confident'
    elif event.confidence > 2.5:
        return 'confident'
    elif event.confidence > 1.5:
        return 'somewhat confident'
    elif event.confidence > .5:
        return 'not very confident'
    else:
        return 'not confident'

def protestPopulationAboveThreshold(event):
    populationProbs = event.getMaxAboveThreshold(event.populationProbs, maxProb)
    stringPopProbs = getPopulationName(populationProbs[0][0]) + ' with probability ' + `round(populationProbs[0][1], 2)`

    # to loop over the other events that are above threshold
    
    for i in range(len(populationProbs)-1):
        (population, prob) = populationProbs[i + 1]
        stringPopProbs = stringPopProbs + ', and' + getPopulationName(population) + ' with probability ' + `round(prob, 2)`
    stringPopProbs = stringPopProbs + '.'
    return stringPopProbs


def protestTypeAboveThreshold(event):
    eventProbs = event.getMaxAboveThreshold(event.eventProbs, maxProb)
    stringEventProbs = `round(eventProbs[0][1], 2)` + ' probability that this event is related to ' + convertEventNumIntoDescriptivePhrase(eventProbs[0][0])

    # to loop over the other events that are above threshold
    
    for i in range(len(eventProbs)-1):
        (eventNum, prob) = eventProbs[i + 1]
        stringEventProbs = stringEventProbs + ', and a ' + `round(prob, 2)` + ' probability that this event is related to ' + convertEventNumIntoDescriptivePhrase(eventNum)
    stringEventProbs = stringEventProbs + '.'
    return stringEventProbs
        
    

def printCriticalInsight(event):
    print 'Critical Insight: Summary of the main conclusion of the forecast'
    print
    print 'Our algorithm forecasts there will be a',
    if event.getMax(event.violenceProbs)[0][0] == '2': 
        print 'violent',
    else:
        print 'nonviolent',
    print 'protest on ' + formatDate(event.date) + ' in ' + event.location[2] + ', ' + event.location[0] + '.',
    print 'We predict the protest will involve' + populationMax(event) + '. The protest will be related to',
    print protestTypeMax(event) + '.'
    print
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

