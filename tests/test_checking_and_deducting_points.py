def test_use_more_points_than_available(client):
    """
    TEST TO COVER BUG #2
    """
    initial_post_data = {
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '10'
    }
    response = client.post('/purchasePlaces', data=initial_post_data)
    assert response.status_code == 302
    # Assert that the redirect is to the /book/<competition>/<club> URL
    assert '/book/Spring%20Festival/Iron%20Temple' in response.headers['Location'] 
    # 2. Extract the Location header and make a new GET request to that URL
    # This GET request will be made within the same test client session,
    # so the flashed message will be available.
    redirect_target_url = response.headers['Location']
    redirect_response = client.get(redirect_target_url)
    assert redirect_response.status_code == 200
    assert b"You do not have enough" in redirect_response.data
    assert b"error" in redirect_response.data
    assert b"Places available" in redirect_response.data

def test_book_more_places_than_available(client):
    """
    BUG #242
    """
    initial_post_data = {
        'competition': 'Fall Classic',
        'club': 'Iron Temple',
        'places': '14'
    }
    response = client.post('/purchasePlaces', data=initial_post_data)
    assert response.status_code == 302
    # Assert that the redirect is to the /book/<competition>/<club> URL
    assert '/book/Fall%20Classic/Iron%20Temple' in response.headers['Location'] 
    # 2. Extract the Location header and make a new GET request to that URL
    # This GET request will be made within the same test client session,
    # so the flashed message will be available.
    redirect_target_url = response.headers['Location']
    redirect_response = client.get(redirect_target_url)
    assert redirect_response.status_code == 200
    assert b"This competition only has" in redirect_response.data
    assert b"error" in redirect_response.data
    assert b"Places available" in redirect_response.data

def test_points_should_be_updated(client):
    """
    TEST TO COVER BUG #6
    """
    pass

def test_zero_points_error(client):
    """
    NOT OFFICIALLY DEFINED AS A BUG
    """
    initial_post_data = {
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '0'
    }
    response = client.post('/purchasePlaces', data=initial_post_data)
    assert response.status_code == 302
    # Assert that the redirect is to the /book/<competition>/<club> URL
    assert '/book/Spring%20Festival/Iron%20Temple' in response.headers['Location'] 
    # 2. Extract the Location header and make a new GET request to that URL
    # This GET request will be made within the same test client session,
    # so the flashed message will be available.
    redirect_target_url = response.headers['Location']
    redirect_response = client.get(redirect_target_url)
    assert redirect_response.status_code == 200
    assert b"at least 1 place" in redirect_response.data
    assert b"error" in redirect_response.data
    assert b"Places available" in redirect_response.data

def test_negative_points_error(client):
    """
    NOT OFFICIALLY DEFINED AS A BUG
    """
    initial_post_data = {
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '-1000'
    }
    response = client.post('/purchasePlaces', data=initial_post_data)
    assert response.status_code == 302
    # Assert that the redirect is to the /book/<competition>/<club> URL
    assert '/book/Spring%20Festival/Iron%20Temple' in response.headers['Location'] 
    # 2. Extract the Location header and make a new GET request to that URL
    # This GET request will be made within the same test client session,
    # so the flashed message will be available.
    redirect_target_url = response.headers['Location']
    redirect_response = client.get(redirect_target_url)
    assert redirect_response.status_code == 200
    assert b"at least 1 place" in redirect_response.data
    assert b"error" in redirect_response.data
    assert b"Places available" in redirect_response.data

def test_no_more_than_twelve_points(client):
    """
    TEST TO COVER BUG #3
    """
    pass