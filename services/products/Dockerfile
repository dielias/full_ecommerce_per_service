FROM python:3.13.5-slim-bookworm

WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY services/products/requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

# Copia o diretório do serviço 'products' para o diretório correto dentro do contêiner
COPY services/products /app/services/products

# Comando para rodar o serviço
CMD ["uvicorn", "services.products.app:app", "--host", "0.0.0.0", "--port", "8002"]
