import psutil
import time
import requests
import csv

# Inicializa o dicionário para guardar as estatísticas
stats = {
    "endpoint": [],
    "cpu_percent": [],
    "memory_percent": [],
    "swap_percent": [],
    "response_time": [],
}

# Endpoints que serão testados
endpoints = [
    "http://localhost:8001/users",    # ajuste se o /users não existir!
    "http://localhost:8002/products",
    "http://localhost:8003/orders",
]

def test_resource_usage_during_requests():
    process = psutil.Process()

    for endpoint in endpoints:
        stats["endpoint"].append(endpoint)

        # Antes da requisição
        memory_before = process.memory_info().rss
        cpu_before = process.cpu_percent(interval=None)
        swap_before = psutil.swap_memory().percent

        start_time = time.time()

        # Fazendo a requisição
        response = requests.get(endpoint)

        elapsed_time = time.time() - start_time

        # Depois da requisição
        memory_after = process.memory_info().rss
        cpu_after = process.cpu_percent(interval=None)
        swap_after = psutil.swap_memory().percent

        # Salvando os dados
        memory_percent = (memory_after - memory_before) / memory_before * 100 if memory_before != 0 else 0
        swap_percent = swap_after - swap_before

        stats["cpu_percent"].append(cpu_after)
        stats["memory_percent"].append(memory_percent)
        stats["swap_percent"].append(swap_percent)
        stats["response_time"].append(elapsed_time)

        print(f"Endpoint: {endpoint}")
        print(f"Memory Before: {memory_before} bytes")
        print(f"Memory After: {memory_after} bytes")
        print(f"CPU Before: {cpu_before}%")
        print(f"CPU After: {cpu_after}%")
        print(f"Elapsed Time: {elapsed_time:.4f} seconds\n")

        # Verifica se a resposta foi bem sucedida
        assert response.status_code == 200, f"Erro no endpoint {endpoint}: Status {response.status_code}"

    # Depois que rodar todos, salvar CSV
    save_stats_to_csv()

def save_stats_to_csv():
    with open("resource_usage_results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Endpoint", "CPU (%)", "Memória (%)", "Swap (%)", "Tempo de Resposta (s)"])

        for i in range(len(stats["endpoint"])):
            writer.writerow([
                stats["endpoint"][i],
                stats["cpu_percent"][i],
                stats["memory_percent"][i],
                stats["swap_percent"][i],
                stats["response_time"][i],
            ])

    print("✅ Resultados salvos em resource_usage_results.csv!")



