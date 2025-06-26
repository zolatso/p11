from server import loadCompetitions
from bs4 import BeautifulSoup
from datetime import datetime

def test_check_old_competition(client):
    """
    TEST TO COVER BUG #5
    """
    data={'email': 'admin@irontemple.com'}
    response = client.post('/showSummary', data=data)
    soup = BeautifulSoup(response.data, 'html.parser')
    assert response.status_code == 200

    # Get two lists of competitions, one with past competitions one with future
    competitions = loadCompetitions()
    now = datetime.now()
    upcoming = []
    finished = []
    for comp in competitions:
        comp_date = datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S")
        if comp_date > now:
            upcoming.append(comp)
        else:
            finished.append(comp)

    # Check that past competitions are listed in <li> elements with <ul> id "past comps"
    for comp in finished:
        li = next((li for li in soup.find_all('li') if li.get_text(strip=True).startswith(comp['name'])),
        None
    )
        assert li is not None, f"<li> starting with '{comp['name']}' not found in response"
        # Check that the same li element does not contain the phrase "book places" or any hyperlinks
        assert "Book Places" not in li.get_text(strip=True)
        assert li.find('a') is None

        ul = li.find_parent('ul')
        assert ul is not None, f"<ul> not found as parent of <li> for club '{comp['name']}'"
        assert ul.get('id') == 'past comps'

    # Opposite test: check that future competitions have "upcoming comps" parent id and a hyperlink
        # Check that past competitions are listed in <li> elements with <ul> id "past comps"
    for comp in upcoming:
        li = next((li for li in soup.find_all('li') if li.get_text(strip=True).startswith(comp['name'])),
        None
    )
        assert li is not None, f"<li> starting with '{comp['name']}' not found in response"
        # Check that the same li element does not contain the phrase "book places" or any hyperlinks
        print(li)
        assert "Book Places" in li.get_text(strip=True)
        assert li.find('a') is not None

        ul = li.find_parent('ul')
        assert ul is not None, f"<ul> not found as parent of <li> for club '{comp['name']}'"
        assert ul.get('id') == 'upcoming comps'
    
