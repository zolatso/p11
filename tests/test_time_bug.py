from server import loadClubs, loadCompetitions

def test_check_old_competition(client):
    """
    TEST TO COVER BUG #5
    """
    data={'email': 'admin@irontemple.com'}
    response = client.post('/showSummary', data=data)
    assert response.status_code == 200
