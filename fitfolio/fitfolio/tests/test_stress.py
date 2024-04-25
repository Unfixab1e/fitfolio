from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def load_activity_data(self):
        self.client.get("/activity", headers={"Authorization": "Bearer testtoken"})
