import pytest
from unittest.mock import patch

class TestPurchasePlacesValidation:
    """
    These tests cover all the ways that invalid data is rejected on the booking page.
    They import basic setup from conftest. 
    """
    def test_use_more_points_than_available(self, client, mock_data_setup):
        """
        TEST TO COVER BUG #2
        """
        mock_data_setup["mock_comps_data"].clear()
        mock_data_setup["mock_comps_data"].extend([{
            "name": "Spring Festival",
            "numberOfPlaces": "25"}])
        mock_data_setup["mock_clubs_data"].clear()
        mock_data_setup["mock_clubs_data"].extend([{
            "name": "Iron Temple", 
            "points": "5"}])
        initial_post_data = {
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '10'
        }
        response = client.post('/purchasePlaces', data=initial_post_data)
        assert response.status_code == 302
        assert '/book/Spring%20Festival/Iron%20Temple' in response.headers['Location'] 
        redirect_target_url = response.headers['Location']
        redirect_response = client.get(redirect_target_url)
        assert redirect_response.status_code == 200
        assert b"You do not have enough" in redirect_response.data
        assert b"error" in redirect_response.data
        assert b"Places available" in redirect_response.data

    def test_book_more_places_than_available(self, client, mock_data_setup):
        """
        BUG #242
        """
        mock_data_setup["mock_comps_data"].clear()
        mock_data_setup["mock_comps_data"].extend([{
            "name": "Spring Festival",
            "numberOfPlaces": "5"}])
        mock_data_setup["mock_clubs_data"].clear()
        mock_data_setup["mock_clubs_data"].extend([{
            "name": "Iron Temple", 
            "points": "10"}])
        initial_post_data = {
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '6'
        }
        response = client.post('/purchasePlaces', data=initial_post_data)
        assert response.status_code == 302
        assert '/book/Spring%20Festival/Iron%20Temple' in response.headers['Location'] 
        redirect_target_url = response.headers['Location']
        redirect_response = client.get(redirect_target_url)
        assert redirect_response.status_code == 200
        assert b"This competition only has" in redirect_response.data
        assert b"error" in redirect_response.data
        assert b"Places available" in redirect_response.data

    def test_no_more_than_twelve_points(self, client, mock_data_setup):
        """
        TEST TO COVER BUG #3
        """
        initial_post_data = {
            'competition': 'X',
            'club': 'Y',
            'places': '13'
        }
        response = client.post('/purchasePlaces', data=initial_post_data)
        assert response.status_code == 302
        assert '/book/X/Y' in response.headers['Location'] 
        redirect_target_url = response.headers['Location']
        redirect_response = client.get(redirect_target_url)
        assert redirect_response.status_code == 200
        assert b"cannot choose more than 12 places" in redirect_response.data
        assert b"error" in redirect_response.data
        assert b"Places available" in redirect_response.data

    def test_zero_points_error(self, client, mock_data_setup):
        """
        NOT OFFICIALLY DEFINED AS A BUG
        """
        initial_post_data = {
            'competition': 'X',
            'club': 'Y',
            'places': '0'
        }
        response = client.post('/purchasePlaces', data=initial_post_data)
        assert response.status_code == 302
        # Assert that the redirect is to the /book/<competition>/<club> URL
        assert '/book/X/Y' in response.headers['Location'] 
        # 2. Extract the Location header and make a new GET request to that URL
        # This GET request will be made within the same test client session,
        # so the flashed message will be available.
        redirect_target_url = response.headers['Location']
        redirect_response = client.get(redirect_target_url)
        assert redirect_response.status_code == 200
        assert b"at least 1 place" in redirect_response.data
        assert b"error" in redirect_response.data
        assert b"Places available" in redirect_response.data

    def test_negative_points_error(self, client, mock_data_setup):
        """
        NOT OFFICIALLY DEFINED AS A BUG
        """
        initial_post_data = {
            'competition': 'X',
            'club': 'Y',
            'places': '-1000'
        }
        response = client.post('/purchasePlaces', data=initial_post_data)
        assert response.status_code == 302
        # Assert that the redirect is to the /book/<competition>/<club> URL
        assert '/book/X/Y' in response.headers['Location'] 
        # 2. Extract the Location header and make a new GET request to that URL
        # This GET request will be made within the same test client session,
        # so the flashed message will be available.
        redirect_target_url = response.headers['Location']
        redirect_response = client.get(redirect_target_url)
        assert redirect_response.status_code == 200
        assert b"at least 1 place" in redirect_response.data
        assert b"error" in redirect_response.data
        assert b"Places available" in redirect_response.data

