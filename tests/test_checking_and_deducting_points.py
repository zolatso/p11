def test_use_more_points_than_available(client):
    initial_post_data = {
        'competition': 'Spring Festival',
        'club': 'Iron Temple',
        'places': '1000000'
    }

    # 1. Perform the POST and check the redirect
    response = client.post('/purchasePlaces', data=initial_post_data)

    assert response.status_code == 302 # Assert that a redirect happened
    # Assert that the redirect is to the /book/<competition>/<club> URL
    # Use .endswith() or 'in' as discussed previously for robustness
    assert '/book/Spring%20Festival/Iron%20Temple' in response.headers['Location'] # URL-encoded spaces


    # 2. Extract the Location header and make a new GET request to that URL
    # This GET request will be made within the same test client session,
    # so the flashed message will be available.
    redirect_target_url = response.headers['Location']
    redirect_response = client.get(redirect_target_url)

    assert redirect_response.status_code == 200 # Expect the target page to load successfully

    # 3. Check for the flashed message on the redirected page
    assert b"You do not have enough points to book" in redirect_response.data
    assert b"error" in redirect_response.data

    # You might also want to check for other content specific to the /book page
    assert b"Places available" in redirect_response.data