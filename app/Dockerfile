# Usa uma imagem base com Python e FastAPI
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expõe a porta que o FastAPI usará
EXPOSE 8000

# Define o comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]