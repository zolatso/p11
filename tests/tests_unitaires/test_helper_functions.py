from server import (
    splitCompetitions, 
    validatePointsPlaces
    )
import pytest
from datetime import datetime, timedelta

# Note: JSON loading and saving functionality tested as part of the
# "test_points_updated.py" integration test
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