import re
from flask import Flask,render_template,request,redirect,flash,url_for
from werkzeug.exceptions import BadRequestKeyError 

from helper_functions import (
    loadClubs,
    loadCompetitions,
    saveClubs,
    saveCompetitions,
    splitCompetitions,
    validatePointsPlaces
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_for_tests' # Use a consistent secret key
app.config['TESTING'] = True # Important for testing, disables error catching for better debugging

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    competitions = loadCompetitions()
    clubs = loadClubs()
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
    # In order to fix BUG 5 (can't book for past competitions) I create two competitions lists
    upcoming, finished = splitCompetitions(competitions)
    return render_template(
        'welcome.html',
        club=found_club,
        finished_competitions=finished,
        upcoming_competitions=upcoming
        )


@app.route('/book/<competition>/<club>')
def book(competition,club):
    competitions = loadCompetitions()
    clubs = loadClubs()
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    """
    There is an issue with the logic of the code here.
    """
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competitions = loadCompetitions()
    clubs = loadClubs()
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesAvailable = int(competition['numberOfPlaces'])
    placesRequired = int(request.form['places'])
    pointsAvailable = int(club['points'])
    valid, error_msg = validatePointsPlaces(placesAvailable, placesRequired, pointsAvailable)
    if not valid:
        flash(error_msg, 'error')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))
    # If all conditions are passed, update points and save the json
    competition['numberOfPlaces'] = placesAvailable - placesRequired
    club['points'] = pointsAvailable - placesRequired
    # Save to the JSON
    saveClubs(clubs)
    saveCompetitions(competitions)
    flash('Great-booking complete!')
    upcoming, finished = splitCompetitions(competitions)
    return render_template(
        'welcome.html',
        club=club,
        finished_competitions=finished,
        upcoming_competitions=upcoming
        )


@app.route('/displayClubs',methods=['GET'])
def displayClubs():
    clubs = loadClubs()
    return render_template('club_display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
