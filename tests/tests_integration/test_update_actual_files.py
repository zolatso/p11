from server import loadClubs, loadCompetitions

def test_points_should_be_updated(client):
    """
    TEST TO COVER BUG #6
    """
    # We are going to load the JSON data at the start to check it is different
    # after we send valid data
    initial_club_list = loadClubs()
    initial_competition_list = loadCompetitions()
    club = initial_club_list[0]
    competition = initial_competition_list[0]
    initial_post_data = {
        'competition': competition['name'],
        'club': club['name'],
        'places': '1'
    }

    response = client.post('/purchasePlaces', data=initial_post_data)
    assert response.status_code == 200
    saved_club_list = loadClubs()
    saved_competition_list = loadCompetitions()

    # Assume their names are still equal
    assert saved_club_list[0]['name'] == club['name']
    # Points should have reduced by 1
    assert saved_club_list[0]['points'] == club['points'] - 1
    # Test competitions in the same way
    assert saved_competition_list[0]['name'] == competition['name']
    assert saved_competition_list[0]['numberOfPlaces'] == competition['numberOfPlaces'] - 1

    # Now check the response message and page are loaded correctly
    assert b"Great-booking complete!" in response.data

    # Add a function here that reverts the data to its original quantity, i.e., adds 1 point


