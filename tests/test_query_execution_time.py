import time
import csv
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from sqlalchemy.engine.url import URL

# Montando a URL de conexão de forma segura
db_config = {
    "drivername": "postgresql+asyncpg",
    "username": "ecommerce",
    "password": "my_password",
    "host": "ecommerce-db",
    "port": 5432,
    "database": "ecommerce"
}

# Cria a engine assíncrona
engine = create_async_engine(URL.create(**db_config))

# Queries que queremos testar
queries = {
    "Listar usuários": "SELECT * FROM users;",
    "Listar produtos": "SELECT * FROM products;",
    "Listar pedidos": "SELECT * FROM orders;",
}

@pytest.mark.asyncio
async def test_query_execution_times():
    results = []

    async with engine.connect() as connection:
        for description, query in queries.items():
            start_time = time.time()
            result = await connection.execute(text(query))
            elapsed_time = time.time() - start_time

            rows_fetched = len(result.fetchall())

            print(f"🔍 {description}: {elapsed_time:.6f} segundos ({rows_fetched} registros)")

            results.append({
                "Descrição": description,
                "Tempo de Execução (s)": elapsed_time,
                "Total de Registros": rows_fetched
            })

    # Salva os resultados em CSV
    with open("query_execution_times.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Descrição", "Tempo de Execução (s)", "Total de Registros"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print("✅ Resultados salvos em query_execution_times.csv!")



