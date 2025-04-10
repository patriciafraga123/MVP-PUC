# filmespop_api – API de Filmes Populares do Projeto My Movies

API secundária do projeto My Movies, responsável por armazenar e gerenciar os filmes populares obtidos a partir da API externa TMDb. Permite salvar em lote os dados de filmes populares vindos da `tmdb_api` no banco, consultar o banco local, cadastrar individualmente e atualizar os campos "Adorei" e "Watchlist".

## Funcionalidades

- Armazenar filmes populares em lote (dados recebidos da API externa `tmdb_api`)
- Inserir manualmente um filme popular
- Listar todos os filmes populares cadastrados
- Atualizar status "adorei" ou "watchlist" de um filme

## Rotas Implementadas

- `POST /salvar-filmes`:  
  Armazena no banco de dados uma lista de filmes populares. 
- `GET /filmespop`:  
  Retorna todos os filmes populares armazenados no banco.
- `POST /salvar-filme`:  
  Salva um único filme popular no banco. Útil para testes ou inserções pontuais.
- `PUT /atualizar-filme`:  
  Atualiza os campos `"adorei"` e `"watchlist"` de um filme popular existente. \


## Estrutura do Projeto

Pasta `filmespop_api/`:

- `pop.py` — Código principal da API de filmes populares
- `model/` — Definição do modelo de dados com SQLAlchemy
- `schemas/` — Schemas de validação Pydantic
- `Dockerfile` — Criação do container Docker da API
- `__init__.py` — Arquivo que transforma este diretório em um pacote Python
- `requirements.txt` — Lista de dependências Python
- `README.md` — Este arquivo

## Integração com o Front-end

Esta API é consumida pelo arquivo index2.html via script script2.js. Faz parte da interface voltada à visualização e marcação de filmes populares.


## Banco de Dados

- A API utiliza um banco PostgreSQL, gerenciado via Docker Compose.
- O nome do banco de dados é `meubanco_filmespop_api`.
- Ele é automaticamente criado na primeira execução do container.

## Executando com Docker Compose

O arquivo `docker-compose.yml` está localizado na **raiz do meufront** (componente principal).

Passos para executar usando o Docker Composer:

1. Certifique-se de que o Docker esteja instalado e em execução.
2. Na raiz do folder meufront, edite o arquivo `docker-compose.yml` para atualizar que a chave `TMDB_API_KEY` que foi informada pela aluna na plataforma da disciplina   *** ATENÇÃO ****
3. No terminal, execute:
docker-compose -p my-movies up -d --build
