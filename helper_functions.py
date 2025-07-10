import json, re
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions
    
def saveClubs(clubs):
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)

def saveCompetitions(competitions):
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)

def splitCompetitions(competitions):
    now = datetime.now()
    upcoming = []
    finished = []
    for comp in competitions:
        comp_date = datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S")
        if comp_date > now:
            upcoming.append(comp)
        else:
            finished.append(comp)
    return upcoming, finished

def validatePointsPlaces(placesAvailable, placesRequired, pointsAvailable):
    # These are organized in such a way that conditions that are independent of actual data are tested first
    if placesRequired <= 0:
        return False, f'You must book at least 1 place'
    # Check user has not asked for more than 12 places - FIXES BUG 4
    if placesRequired > 12:
        return False, f'You cannot choose more than 12 places per competition, please choose fewer places'
    # Check user has not asked for more places than the competition has - BUG 242
    if placesRequired > placesAvailable:
        return False, f'This competition only has {placesAvailable} places available, please choose fewer places'
    # Checks that club has enough points - FIXES BUG 2
    if placesRequired > pointsAvailable:
        return False, f'You do not have enough points to book that many places. You only have {pointsAvailable} points available'
    else:
        return True, 'Data are valid'



         
