from server import (
    loadClubs, 
    loadCompetitions, 
    saveClubs, 
    saveCompetitions, 
    splitCompetitions, 
    validatePointsPlaces
    )
import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import mock_open, patch

# ---------- Tests for loadClubs ----------

def test_loadClubs_happy_path():
    mock_data = {'clubs': [{'name': 'Test Club', 'points': '10'}]}
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        clubs = loadClubs()
        assert isinstance(clubs, list)
        assert clubs[0]['name'] == 'Test Club'

def test_loadClubs_sad_path_invalid_json():
    with patch('builtins.open', mock_open(read_data="not valid json")):
        with pytest.raises(json.JSONDecodeError):
            loadClubs()

# ---------- Tests for loadCompetitions ----------

def test_loadCompetitions_happy_path():
    mock_data = {'competitions': [{'name': 'Comp 1', 'date': '2099-01-01 10:00:00'}]}
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        competitions = loadCompetitions()
        assert isinstance(competitions, list)
        assert competitions[0]['name'] == 'Comp 1'

def test_loadCompetitions_sad_path_missing_key():
    mock_data = {'wrong_key': []}
    with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
        with pytest.raises(KeyError):
            loadCompetitions()

# ---------- Tests for saveClubs / saveCompetitions ----------

def test_saveClubs_happy_path():
    clubs = [{'name': 'Test Club', 'points': '20'}]
    with patch('builtins.open', mock_open()) as m:
        saveClubs(clubs)
        m.assert_called_once_with('clubs.json', 'w')

def test_saveCompetitions_happy_path():
    comps = [{'name': 'Test Comp', 'date': '2099-01-01 00:00:00'}]
    with patch('builtins.open', mock_open()) as m:
        saveCompetitions(comps)
        m.assert_called_once_with('competitions.json', 'w')

# ---------- Tests for splitCompetitions ----------

def test_splitCompetitions_happy_path():
    now = datetime.now()
    comps = [
        {'name': 'Upcoming', 'date': (now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")},
        {'name': 'Past', 'date': (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")}
    ]
    upcoming, finished = splitCompetitions(comps)
    assert len(upcoming) == 1
    assert len(finished) == 1
    assert upcoming[0]['name'] == 'Upcoming'
    assert finished[0]['name'] == 'Past'

def test_splitCompetitions_sad_path_invalid_date():
    comps = [{'name': 'InvalidDateComp', 'date': 'not-a-date'}]
    with pytest.raises(ValueError):
        splitCompetitions(comps)

# Test validatePointsPlaces

def test_validatePointsPlaces_happy_path():
    result, message = validatePointsPlaces(10, 5, 8)
    assert result is True
    assert message == 'Data are valid'

def test_validatePointsPlaces_zero_places():
    result, message = validatePointsPlaces(10, 0, 10)
    assert result is False
    assert 'at least 1 place' in message

def test_validatePointsPlaces_too_many_requested():
    result, message = validatePointsPlaces(5, 6, 10)
    assert result is False
    assert 'only has 5 places' in message

def test_validatePointsPlaces_over_limit_12():
    result, message = validatePointsPlaces(20, 13, 20)
    assert result is False
    assert 'more than 12 places' in message

def test_validatePointsPlaces_insufficient_points():
    result, message = validatePointsPlaces(10, 8, 5)
    assert result is False
    assert 'do not have enough points' in message