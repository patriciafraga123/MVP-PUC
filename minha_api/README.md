# minha_api – Componente Secundário do Projeto My Movies

API secundária do projeto **My Movies**, responsável pelo gerenciamento da lista de filmes pessoais do usuário. Permite cadastrar, consultar, atualizar e remover filmes, bem como associar nota pessoal e status de "assistido".

## Funcionalidades

- Adicionar filmes à lista pessoal
- Buscar filmes por nome ou listar todos
- Atualizar nota pessoal ou status "assistido"
- Remover filmes do banco

## Rotas Implementadas

- `GET /filmes`: Lista todos os filmes cadastrados
- `GET /filme?nome_filme=...`: Retorna informações de um filme específico
- `POST /filme`: Adiciona um novo filme à base local
- `PUT /filme`: Atualiza nota pessoal ou status de assistido
- `DELETE /filme?nome_filme=...`: Remove o filme informado da base de dados

## Estrutura do Projeto
minha_api/ 
─ app.py/ # Código principal da API Flask 
─ logger.py/ # Sistema de logging centralizado 
─ __init__.py/ # Arquivo que transforma este diretório em um pacote Python 
─ model/ # Definição do banco via SQLAlchemy 
─ schemas/ # Schemas de validação  
─ Dockerfile # Criação do container da API 
─ docker-compose.yml # # Orquestrador de todos os componentes da aplicação (minha_api, filmespop_api, tmdb_api, meufront)
─ requirements.txt       # Lista de dependências Python do projeto
─ README.md # Instruções específicas deste Componente 

Pasta `meufront/`:

- `images/` — Imagens usadas no front
- `index.html` — Página principal (My Area)
- `index2.html` — Página de filmes populares (Most Popular Movies)
- `script.js` — JS da index.html (minha lista)
- `scripts2.js` — JS da index2.html (filmes populares)
- `style.css` — Estilo das páginas (usado em ambas as páginas)
- `README.md` — Instruções específicas deste componente
- `READMEGERAL.md` — Instruções gerais da aplicação



## Banco de Dados

Este componente utiliza um banco de dados PostgreSQL isolado, criado automaticamente via Docker Compose. O nome do banco é `meubanco_minha_api`.

## Executando com Docker Compose

O arquivo `docker-compose.yml` está localizado na **raiz do meufront** (componente principal).

Passos para executar usando o Docker Composer:

1. Certifique-se de que o Docker esteja instalado e em execução.
2. Na raiz do folder meufront, edite o arquivo `docker-compose.yml` para atualizar que a chave `TMDB_API_KEY` que foi informada pela aluna na plataforma da disciplina   *** ATENÇÃO ****
3. No terminal, execute:
docker-compose -p my-movies up -d --build

