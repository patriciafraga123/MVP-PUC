# Dockerfile para minha-api
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da API
COPY . .

# Define variáveis de ambiente
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py  

# Comando para rodar a API
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
