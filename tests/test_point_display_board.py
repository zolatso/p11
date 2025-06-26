from server import loadClubs

def test_point_display_board(client):
    "tests feature 5"
    response = client.get('/displayClubs')
    assert response.status_code == 200

    assert b"List of all the clubs currently active" in response.data
    clubs = loadClubs()
    for club in clubs:
        assert str(club['name']).encode() in response.data
        assert str(club['points']).encode() in response.data