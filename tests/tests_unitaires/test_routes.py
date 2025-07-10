from server import (
    loadClubs
)

def test_index_page(client):
    """
    Test the root (index) page to ensure it loads correctly.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Please enter your secretary email to continue:" in response.data

def test_booking_page_opens_correctly(client):
    """
    Test the url format book/<competition>/<club> 
    shows the correct page if proper data found
    """
    response = client.get('book/Spring%20Festival/Iron%20Temple')
    assert response.status_code == 200
    assert b"Spring Festival" in response.data
    assert b"How many places?" in response.data

def test_point_display_board(client):
    "tests feature 5"
    response = client.get('/displayClubs')
    assert response.status_code == 200
    assert b"List of all the clubs currently active" in response.data
    clubs = loadClubs()
    for club in clubs:
        assert str(club['name']).encode() in response.data
        assert str(club['points']).encode() in response.data

def test_logout(client):
    """
    Test logout page
    """
    response = client.get('/logout')
    assert response.status_code == 302
    redirect_target_url = response.headers['Location']
    redirect_response = client.get(redirect_target_url)
    assert b"Welcome to the GUDLFT Registration Portal!" in redirect_response.data
    assert b"Please enter your secretary email to continue:" in redirect_response.data



