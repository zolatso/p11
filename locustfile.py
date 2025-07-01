from locust import HttpUser, task, between
import random

# Dummy test data from your test DB or JSON (adjust accordingly)
VALID_EMAIL = "admin@irontemple.com"
VALID_CLUB_NAME = "Iron Temple"
VALID_COMPETITION_NAME = "Spring Festival"

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Simulates real users waiting between actions

    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": VALID_EMAIL})

    @task
    def book(self):
        self.client.get(f"/book/{VALID_COMPETITION_NAME}/{VALID_CLUB_NAME}")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "club": VALID_CLUB_NAME,
                "competition": VALID_COMPETITION_NAME,
                "places": "1"
            }
        )

    @task
    def display_clubs(self):
        self.client.get("/displayClubs")

    @task
    def logout(self):
        self.client.get("/logout")