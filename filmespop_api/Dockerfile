# Usa uma imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app  

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da API de filmespop e o diretório da minha_api
COPY . .


# Define a variável de ambiente para encontrar `minha_api`
ENV PYTHONPATH=/app  
ENV FLASK_APP=pop.py


# Expõe a porta correta
EXPOSE 5002

# Comando para rodar a API
CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]