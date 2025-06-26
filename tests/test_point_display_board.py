from server import loadClubs
from bs4 import BeautifulSoup

def test_point_display_feature(client):
    """
    TEST TO COVER FEATURE #7
    """
    clubs = loadClubs()
    # Arbitrarily pick first club in the data to login to the site with
    selected_club = clubs[0]
    # We will check other clubs are displayed in the correct place
    other_clubs = clubs[1:]

    data={'email': selected_club['email']}
    response = client.post('/showSummary', data=data)
    soup = BeautifulSoup(response.data, 'html.parser')

    assert response.status_code == 200
    print(response.data.decode())
    # All other clubs should have their name at the start of a <li> element
    # Whose parent is a <ul> with the id "other clubs"
    for club in other_clubs:
        li = next((li for li in soup.find_all('li') if li.get_text(strip=True).startswith(club['name'])),
        None
    )
        assert li is not None, f"<li> starting with '{club['name']}' not found in response"

        ul = li.find_parent('ul')
        assert ul is not None, f"<ul> not found as parent of <li> for club '{club['name']}'"
        assert ul.get('id') == 'other clubs'

    welcome_message = f"Welcome {selected_club['name']}"

    assert welcome_message.encode() in response.data



    
    

