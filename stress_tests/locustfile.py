from locust import HttpUser, task, between
import random
import uuid

class EcommerceUser(HttpUser):
    wait_time = between(1, 2)

    user_id = None
    product_id = None
    order_id = None

    # URLs dos proxies do ToxiProxy
    users_url = "http://localhost:8475"
    products_url = "http://localhost:8476"
    orders_url = "http://localhost:8477"

    def on_start(self):
        # Criar usuário via proxy do ToxiProxy
        name = f"User{random.randint(1, 100000)}"
        email = f"user_{uuid.uuid4()}@test.com"
        response = self.client.post(f"{self.users_url}/users", json={"name": name, "email": email})
        if response.status_code in (200, 201):
            self.user_id = response.json().get("id")

        # Criar produto via proxy do ToxiProxy
        name = f"Product{random.randint(1, 100000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        response = self.client.post(f"{self.products_url}/products", json={"name": name, "price": price})
        if response.status_code in (200, 201):
            self.product_id = response.json().get("id")

    @task(4)
    def create_order(self):
        if self.user_id and self.product_id:
            try:
                response = self.client.post(
                    f"{self.orders_url}/orders",
                    json={"user_id": self.user_id, "product_id": self.product_id},
                    timeout=10
                )
                if response.status_code in (200, 201):
                    self.order_id = response.json().get("id")
            except Exception as e:
                print(f"Falha ao criar pedido: {e}")

    @task(2)
    def list_orders(self):
        try:
            self.client.get(f"{self.orders_url}/orders", timeout=10)
        except Exception as e:
            print(f"Falha ao listar pedidos: {e}")

    @task(1)
    def list_users(self):
        try:
            self.client.get(f"{self.users_url}/users", timeout=10)
        except Exception as e:
            print(f"Falha ao listar usuários: {e}")

    @task(1)
    def list_products(self):
        try:
            self.client.get(f"{self.products_url}/products", timeout=10)
        except Exception as e:
            print(f"Falha ao listar produtos: {e}")

    @task(1)
    def create_user(self):
        name = f"User{random.randint(1, 100000)}"
        email = f"user_{uuid.uuid4()}@test.com"
        try:
            self.client.post(f"{self.users_url}/users", json={"name": name, "email": email}, timeout=10)
        except Exception as e:
            print(f"Falha ao criar usuário: {e}")

    @task(1)
    def create_product(self):
        name = f"Product{random.randint(1, 100000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        try:
            self.client.post(f"{self.products_url}/products", json={"name": name, "price": price}, timeout=10)
        except Exception as e:
            print(f"Falha ao criar produto: {e}")
