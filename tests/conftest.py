import pytest
from server import app as flask_app

@pytest.fixture
def app():
    # Update config here if needed, e.g., for testing
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_data_setup(mocker):
    """Fixture to set up generic mocks for purchasePlaces tests."""
    # Define placeholder initial mock data (can be empty or minimal)
    mock_comps = [{"name":"X", "date": "2026-03-27 10:00:00", "numberOfPlaces":"10"}]
    mock_clubs = [{"name":"Y", "email": "person@validemail.com", "points": "5"}]

    # Patch the functions, but their return_value can be set dynamically per test
    # Or you can set a default and override it
    mocker.patch('server.loadCompetitions', return_value=mock_comps)
    mocker.patch('server.loadClubs', return_value=mock_clubs)

    mock_save_clubs = mocker.patch('server.saveClubs')
    mock_save_competitions = mocker.patch('server.saveCompetitions')

    # Yield a dictionary or tuple of the mock objects for the test to use
    yield {
        "mock_comps_data": mock_comps, # A reference to the list that loadCompetitions returns
        "mock_clubs_data": mock_clubs, # A reference to the list that loadClubs returns
        "save_clubs_mock": mock_save_clubs,
        "save_competitions_mock": mock_save_competitions
    }
