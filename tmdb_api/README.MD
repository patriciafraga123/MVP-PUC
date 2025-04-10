# tmdb_api – API de Integração com The Movie Database (TMDB)

Componente intermediário do projeto My Movies, responsável por integrar a aplicação à API pública do TMDB. Fornece os dados necessários para enriquecer a experiência do usuário com informações atualizadas sobre filmes, como nota da crítica e listagem de filmes populares.

## Funcionalidades

- Consultar a nota (média de avaliação) de um filme usando a API externa do TMDB
- Obter uma lista de filmes populares em tempo real

## Rotas Implementadas

- `GET /nota?filme=nome_do_filme`:  
  Consulta a nota média de um filme informando seu nome. Utiliza o endpoint `/search/movie` da API TMDB.

- `GET /populares`:  
  Retorna a lista atualizada de filmes populares. Utiliza o endpoint `/movie/popular` da API TMDB.

## Requisitos

- Esta API depende de uma chave de acesso pessoal (`TMDB_API_KEY`) da aluna, obtida no site do TMDB
- A chave foi informada junto com a publicação do MVP, na plataforma da disciplina
- A chave deve ser informada como variável de ambiente ou diretamente no `docker-compose.yml`.

## Estrutura do Projeto

tmdb_api/  
─ tmdb.py # Código principal da API Flask de integração externa  
─ Dockerfile # Criação do container Docker da API 
- __init__.py # Arquivo que transforma este diretório em um pacote Python 
─ requirements.txt # Lista de dependências Python  
─ README.md # Este arquivo  

## Integração com o Sistema

Esta API é consumida por dois componentes do projeto My Movies:

- `minha_api`: utiliza a rota `/nota` para buscar a nota de um filme durante o cadastro na lista pessoal.
- `filmespop_api`: utiliza a rota `/populares` para obter os dados mais recentes de filmes populares e salvá-los localmente.

## API Externa Utilizada

- Plataforma [The Movie Database (TMDB)](https://www.themoviedb.org/)
- Base URL: `https://api.themoviedb.org/3`
- Licença: Uso gratuito com cadastro
- Autenticação: Chave de API (API Key) obrigatória


## Executando com Docker Compose

O arquivo `docker-compose.yml` está localizado na **raiz do meufront** (componente principal).

Passos para executar usando o Docker Composer:

1. Certifique-se de que o Docker esteja instalado e em execução.
2. Na raiz do folder meufront, edite o arquivo `docker-compose.yml` para atualizar que a chave `TMDB_API_KEY` que foi informada pela aluna na plataforma da disciplina   *** ATENÇÃO ****
3. No terminal, execute:
docker-compose -p my-movies up -d --build


