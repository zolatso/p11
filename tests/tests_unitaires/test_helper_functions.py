from server import (
    loadClubs, 
    loadCompetitions, 
    saveClubs, 
    saveCompetitions, 
    splitCompetitions, 
    validatePointsPlaces
    )

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