# Test cases for showSummary
def test_show_summary_valid_email_found(client):
    """
    Test when a valid email is provided and found in clubs.
    Should render welcome.html with club and competitions data.
    """
    response = client.post('/showSummary', data={'email': 'admin@irontemple.com'})
    assert response.status_code == 200
    assert b"Points available" in response.data # Check for a specific string from welcome.html
    assert b"admin@irontemple.com" in response.data # Check if the club email is displayed

def test_show_summary_invalid_email_format(client):
    """
    Test when an email with an invalid format is provided.
    Should redirect to index and flash an error message.
    """
    response = client.post('/showSummary', data={'email': 'invalid-email'})
    assert response.status_code == 302 # Expect a redirect
    assert response.headers['Location'].endswith('/') # Should redirect to the root URL

    # Follow the redirect to check the flashed message
    redirect_response = client.get('/')
    assert b"Invalid email address format. Please enter a valid email." in redirect_response.data
    assert b"error" in redirect_response.data # Check for the category class

def test_show_summary_email_not_found(client):
    """
    Test when a validly formatted email is provided but not found in clubs.
    Should redirect to index and flash an error message.
    """
    response = client.post('/showSummary', data={'email': 'nonexistent@example.com'})
    assert response.status_code == 302 # Expect a redirect
    assert response.headers['Location'].endswith('/') # Should redirect to the root URL

    # Follow the redirect to check the flashed message
    redirect_response = client.get('/')
    assert b"Email address not found in our records. Please try again or register." in redirect_response.data
    assert b"error" in redirect_response.data # Check for the category class

def test_show_summary_no_email_provided(client):
    """
    Test when no email is provided (empty form submission).
    Should redirect to index and flash an error message.
    """
    response = client.post('/showSummary', data={'email': ''}) # Or just client.post('/showSummary') for no data
    assert response.status_code == 302 # Expect a redirect
    assert response.headers['Location'].endswith('/')

    redirect_response = client.get('/')
    assert b"Invalid email address format. Please enter a valid email." in redirect_response.data
    assert b"error" in redirect_response.data

def test_index_page(client):
    """
    Test the root (index) page to ensure it loads correctly.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"Please enter your secretary email to continue:" in response.data