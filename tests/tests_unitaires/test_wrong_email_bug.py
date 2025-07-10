import pytest

@pytest.mark.usefixtures("mock_data_setup")
class TestShowSummaryRoute:
    """
    Test suite for the /showSummary route, covering various email input scenarios.
    """
    VALID_TEST_EMAIL = "person@validemail.com"

    def test_show_summary_invalid_email_format(self, client):
        """
        BUG #1
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

    def test_show_summary_email_not_found(self, client):
        """
        BUG #1
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

    def test_show_summary_no_email_provided(self, client):
        """
        BUG #1
        Test when no email is provided (empty form submission).
        Should redirect to index and flash an error message.
        """
        response = client.post('/showSummary', data={'email': ''}) # Or just client.post('/showSummary') for no data
        assert response.status_code == 302 # Expect a redirect
        assert response.headers['Location'].endswith('/')

        redirect_response = client.get('/')
        assert b"Invalid email address format. Please enter a valid email." in redirect_response.data
        assert b"error" in redirect_response.data

    def test_show_summary_valid_email_found(self, client):
        """
        Test when a valid email is provided and found in clubs.
        Should render welcome.html with club and competitions data.
        Note there is a more specific test to check the way I have handled past/future competitions.
        See "test_time_bug.py"
        """
        response = client.post('/showSummary', data={'email': self.VALID_TEST_EMAIL})
        assert response.status_code == 200
        assert b"points available" in response.data
        assert self.VALID_TEST_EMAIL in response.text


