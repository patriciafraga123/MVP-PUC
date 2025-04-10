# Usa uma imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /tmdb

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte para dentro do container
COPY . .

# Define variáveis de ambiente para o Flask
ENV FLASK_APP=tmdb.py  
ENV FLASK_RUN_HOST=0.0.0.0  
ENV FLASK_RUN_PORT=5001  
ENV PYTHONUNBUFFERED=1  

# Expõe a porta correta
EXPOSE 5001

# Comando para rodar a API
CMD ["flask", "run"]

