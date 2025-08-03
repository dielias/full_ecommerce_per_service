FROM python:3.13.5-slim-bookworm

WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY services/db-init/requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

# Copia o diretório completo 'services' para o diretório /app no contêiner
COPY services /app/services

# Define o PYTHONPATH para o diretório /app, assim o Python poderá localizar 'services'
ENV PYTHONPATH=/app

# Comando para inicializar os bancos de dados
CMD ["python", "/app/services/db-init/init_db.py"]



