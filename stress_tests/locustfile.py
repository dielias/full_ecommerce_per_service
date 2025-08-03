from locust import HttpUser, task, between
import random

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)

    user_id = None
    product_id = None
    order_id = None

    def on_start(self):
        # Criar usuário e salvar ID
        name = f"User{random.randint(1, 100000)}"
        email = f"{name.lower()}@test.com"
        response = self.client.post("http://users:8001/users", json={"name": name, "email": email})
        if response.status_code in (200, 201):
            self.user_id = response.json().get("id")

        # Criar produto e salvar ID
        name = f"Product{random.randint(1, 100000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        response = self.client.post("http://products:8002/products", json={"name": name, "price": price})
        if response.status_code in (200, 201):
            self.product_id = response.json().get("id")

    @task(4)
    def create_order(self):
        if self.user_id and self.product_id:
            response = self.client.post("http://orders:8003/orders", json={"user_id": self.user_id, "product_id": self.product_id})
            if response.status_code in (200, 201):
                self.order_id = response.json().get("id")

    @task(2)
    def list_orders(self):
        self.client.get("http://orders:8003/orders")

    @task(1)
    def list_users(self):
        self.client.get("http://users:8001/users")

    @task(1)
    def list_products(self):
        self.client.get("http://products:8002/products")

    @task(1)
    def create_user(self):
        name = f"User{random.randint(1, 100000)}"
        email = f"{name.lower()}@test.com"
        self.client.post("http://users:8001/users", json={"name": name, "email": email})

    @task(1)
    def create_product(self):
        name = f"Product{random.randint(1, 100000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        self.client.post("http://products:8002/products", json={"name": name, "price": price})
        