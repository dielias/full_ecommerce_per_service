from locust import HttpUser, task, between
import random

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def create_user(self):
        name = f"User{random.randint(1, 10000)}"
        email = f"{name.lower()}@test.com"
        self.client.post("http://users:8001/users", json={"name": name, "email": email})

    @task(2)
    def create_product(self):
        name = f"Product{random.randint(1, 10000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        self.client.post("http://products:8002/products", json={"name": name, "price": price})

    @task(4)
    def create_order(self):
        # Para teste, usar IDs genéricos (ideal: criar fixtures para usuários/produtos)
        self.client.post("http://orders:8003/orders", json={"user_id": 1, "product_id": 1})

    @task(1)
    def list_orders(self):
        self.client.get("http://orders:8003/orders")
