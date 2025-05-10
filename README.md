 Full Ecommerce API - Microservices Architecture

Este projeto é uma aplicação de ecommerce implementada com **FastAPI**, estruturada com **arquitetura de microserviços** e utilizando o padrão **Per Service Database** e **API Composition** para integração.

## 🧱 Estrutura do Projeto

```
.
├── docker-compose.yml
├── services
│   ├── api-composer        # Serviço que compõe dados dos outros microserviços
│   ├── users               # Microserviço de usuários
│   ├── products            # Microserviço de produtos
│   ├── orders              # Microserviço de pedidos
│   └── db-init             # Inicialização dos bancos
├── tests                   # Testes automatizados
```

Cada microserviço possui seu próprio banco de dados PostgreSQL e API independente.

## 🚀 Como Executar

### Pré-requisitos

- Docker
- Docker Compose
- Python 3.12

### Subir os serviços

```bash
docker compose up --build
```

Isso inicializa todos os serviços e bancos de dados. A aplicação estará disponível nos seguintes endpoints:

| Serviço      | Porta | Endereço Base         |
|--------------|-------|------------------------|
| Users        | 8001  | `http://localhost:8001` |
| Products     | 8002  | `http://localhost:8002` |
| Orders       | 8003  | `http://localhost:8003` |

## 🔌 Endpoints

### Users

- `GET /users`
- `GET /users/{user_id}`
- `POST /users`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

### Products

- `GET /products`
- `GET /products/{product_id}`
- `POST /products`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`

### Orders

- `GET /orders`
- `GET /orders/{order_id}`
- `POST /orders`
- `PUT /orders/{order_id}`
- `DELETE /orders/{order_id}`

## 🧪 Testes

Para rodar os testes (fora do docker):

```bash
cd tests
pytest
```

## 📦 Tecnologias

- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose
- Pydantic
- Pytest

## 🛠️ Arquitetura

- **Per Service Database**: Cada microserviço possui seu próprio banco PostgreSQL.
- **Isolamento total**: Microserviços não compartilham modelos ou banco de dados.

## 📝 Licença

Este projeto está licenciado sob a licença MIT.

