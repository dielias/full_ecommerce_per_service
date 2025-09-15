from locust import HttpUser, task, between
import random
import uuid

class EcommerceUser(HttpUser):
    wait_time = between(1, 2)

    # URLs dos endpoints
    users_url = "http://users:8001"
    products_url = "http://products:8002"
    orders_url = "http://orders:8003"

    user_id = None
    product_id = None

    def on_start(self):
        # Apenas prepara os dados necessários para o teste
        # Cria um usuário e um produto para que os pedidos possam ser criados
        response = self.client.post(f"{self.users_url}/users", json={"name": f"User{random.randint(1, 100000)}", "email": f"user_{uuid.uuid4()}@test.com"})
        if response.status_code in (200, 201):
            self.user_id = response.json().get("id")

        response = self.client.post(f"{self.products_url}/products", json={"name": f"Product{random.randint(1, 100000)}", "price": round(random.uniform(10.0, 100.0), 2), "quantity": random.randint(1, 100)})
        if response.status_code in (200, 201):
            self.product_id = response.json().get("id")

    @task(4)
    # Cria pedido
    def create_order(self):
        if self.user_id and self.product_id:
            self.client.post(f"{self.orders_url}/orders", json={"user_id": self.user_id, "product_id": self.product_id})

    @task(2)
    # Lista pedidos
    def list_orders(self):
        self.client.get(f"{self.orders_url}/orders")

    @task(1)
    # Lista usuários
    def list_users(self):
        self.client.get(f"{self.users_url}/users")

    @task(1)
    # Lista produtos
    def list_products(self):
        self.client.get(f"{self.products_url}/products")

    @task(1)
    # Cria usuário
    def create_user(self):
        name = f"User{random.randint(1, 100000)}"
        email = f"user_{uuid.uuid4()}@test.com"
        self.client.post(f"{self.users_url}/users", json={"name": name, "email": email})

    @task(1)
    # Cria produto
    def create_product(self):
        name = f"Product{random.randint(1, 100000)}"
        price = round(random.uniform(10.0, 100.0), 2)
        quantity = random.randint(1, 100)
        self.client.post(f"{self.products_url}/products", json={"name": name, "price": price, "quantity": quantity})