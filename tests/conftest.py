import pytest
from server import app as flask_app

@pytest.fixture
def app():
    # Update config here if needed, e.g., for testing
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()