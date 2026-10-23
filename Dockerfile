
# Imagem base com Python 3.11
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia a lista de dependencias
COPY requirements.txt .

# Instala as dependencias do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo e os testes
COPY src/ ./src/
COPY tests/ ./tests/

# Comando executado ao iniciar o container
CMD ["python", "-m", "pytest", "tests/test_harness.py", "-v"]
