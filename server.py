import json, re
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_for_tests' # Use a consistent secret key
app.config['TESTING'] = True # Important for testing, disables error catching for better debugging

competitions = loadCompetitions()
clubs = loadClubs()
app.clubs = clubs
app.competitions = competitions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email_input = request.form['email']
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_input):
        flash('Invalid email address format. Please enter a valid email.', 'error')
        return redirect(url_for('index'))
    found_club = None
    for club in clubs:
        if club['email'] == email_input:
            found_club = club
            break
    if found_club is None:
        flash('Email address not found in our records. Please try again or register.', 'error')
        return redirect(url_for('index'))
    return render_template(
        'welcome.html',
        club=found_club,
        competitions=competitions,
        )


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesAvailable = int(competition['numberOfPlaces'])
    placesRequired = int(request.form['places'])
    pointsAvailable = int(club['points'])
    # Check user has entered positive number - FIXES BUG I IDENTIFIED
    if placesRequired <= 0:
        flash(f'You must book at least 1 place', 'error')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    # Check user has not asked for more places than the competition has - BUG 242
    if placesRequired > placesAvailable:
        flash(f'This competition only has {placesAvailable} places available, please choose fewer places', 'error')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    # Check user has not asked for more than 12 places - FIXES BUG 4
    if placesRequired > 12:
        flash(f'You cannot choose more than 12 places per competition, please choose fewer places', 'error')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    # Checks that club has enough points - FIXES BUG 2
    if placesRequired > pointsAvailable:
        flash(f'You do not have enough points to book that many places. You only have {pointsAvailable} points available', 'error')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))      
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
