from locust import HttpUser, task, between
import random
import os
import uuid

class EcommerceUser(HttpUser):
    wait_time = between(1, 2)

    user_id = None
    product_id = None
    order_id = None

    # URLs dos proxies do ToxiProxy
    users_url = "http://users:8001"
    products_url = "http://products:8002"
    orders_url = "http://orders:8003"

    def on_start(self):
        try:
            # Criar usuário via proxy do ToxiProxy
            name = f"User{random.randint(1, 100000)}"
            email = f"user_{uuid.uuid4()}@test.com"
            response = self.client.post(f"{self.users_url}/users", json={"name": name, "email": email})
            if response.status_code in (200, 201):
                self.user_id = response.json().get("id")
            else:
                print(f"Failed to create user: Status {response.status_code}")

            # Criar produto via proxy do ToxiProxy
            name = f"Product{random.randint(1, 100000)}"
            price = round(random.uniform(10.0, 100.0), 2)
            quantity = random.randint(1, 100)
            response = self.client.post(
                f"{self.products_url}/products", 
                json={"name": name, "price": price,"quantity": quantity})
            if response.status_code in (200, 201):
                self.product_id = response.json().get("id")
            else:
                print(f"Failed to create product: Status {response.status_code}")

        except Exception as e:
                print(f"Exception during create_order: {e}")

    @task(4)
    def create_order(self):
        if self.user_id and self.product_id:
            try:
                response = self.client.post(
                    f"{self.orders_url}/orders",
                    json={"user_id": self.user_id, "product_id": self.product_id}
                )
                if response.status_code in (200, 201):
                    self.order_id = response.json().get("id")
                else:
                    print(f"Failed to create order: Status {response.status_code}")
            except Exception as e:
                print(f"Exception during create_order: {e}")

    @task(2)
    def list_orders(self):
        try:
            self.client.get(f"{self.orders_url}/orders")
        except Exception as e:
            print(f"Falha ao listar pedidos: {e}")

    @task(1)
    def list_users(self):
        try:
            self.client.get(f"{self.users_url}/users")
        except Exception as e:
            print(f"Falha ao listar usuários: {e}")

    @task(1)
    def list_products(self):
        try:
            self.client.get(f"{self.products_url}/products")
        except Exception as e:
            print(f"Falha ao listar produtos: {e}")

    @task(1)
    def create_user(self):
        name = f"User{random.randint(1, 100000)}"
        email = f"user_{uuid.uuid4()}@test.com"
        try:
            response = self.client.post(f"{self.users_url}/users", json={"name": name, "email": email})
            if response.status_code not in (200, 201):
                print(f"Failed to create user: Status {response.status_code}")
        except Exception as e:
            print(f"Exception during create_user: {e}")

    @task(1)
    def create_product(self):
        name = f"Product{random.randint(1, 100000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        quantity = random.randint(1, 100)

        try:
            response = self.client.post(
                f"{self.products_url}/products", 
                json={"name": name, "price": price, "quantity": quantity}
                )
            if response.status_code not in (200, 201):
                print(f"Failed to create product: Status {response.status_code}")
        except Exception as e:
            print(f"Exception during create_product: {e}")
