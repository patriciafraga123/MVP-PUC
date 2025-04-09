# My Movies – Gerenciador de Filmes

Projeto da Pós-Graduação em Engenharia de Software – PUC-Rio**
Aluna :  Patricia Fraga  
Data: Abril/2025  

# Descrição Geral

O projeto My Movies é uma aplicação  composta por múltiplas APIs e uma interface web que permite ao usuário cadastrar, consultar, atualizar e remover informações sobre filmes. A aplicação também se conecta à API externa pública TMDB para consultar notas e listas de filmes populares.

## Fluxograma

Aqui está um fluxograma que ilustra o funcionamento do projeto:

![Fluxograma](minha_api/fluxograma.png)

# Componentes do Projeto

| Componente       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| `minha_api`      | **API principal** que gerencia o banco de dados de filmes do usuário       |
| `filmespop_api`  | API secundária que gerencia filmes populares armazenados no banco         |
| `tmdb_api`       | API intermediária que se comunica com a API externa do TMDB       |
| `meufront`       | Interface do usuário (HTML/CSS/JavaScript)                                |

# Diagrama da Arquitetura

## Descrição dos Componentes de Back-End

`minha_api` – API Principal
API responsável por gerenciar a lista de filmes pessoais do usuário. Permite adicionar, buscar, atualizar ou remover filmes, além de associar uma nota pessoal e marcar se o filme foi assistido. Toda a lógica de CRUD (Create, Read, Update, Delete) da área "Minha Lista" é controlada por esta API.

`filmespop_api` – API Secundária
API que gerencia uma cópia local de filmes populares, originalmente obtidos via TMDB. Permite que o usuário armazene e personalize esses filmes localmente, adicionando marcações como “quero assistir” 👁️ ou “adorei” ❤️.

`tmdb_api` – API Intermediária
API responsável por fazer chamadas diretas à API externa do TMDB. Atua como intermediária para proteger a chave de acesso, evitando exposição no front-end. Fornece informações externas como nota e lista de filmes populares, enriquecendo a aplicação com dados reais.

# Interface do Usuário (`meufront`)

A interface foi construída com HTML, CSS e JavaScript puro, sem frameworks. Ela  é composta por duas páginas principais:

a) index.html – Minha Área

Página principal da aplicação, com foco na gestão pessoal dos filmes

Funcionalidades:
- Adicionar um novo filme, buscando a nota do filme da APIO TMDB
- Listar todos os filmes cadastrados nas listas My Ratigs ou My Watchlist
- Atualizar um filme da lista My Watchlist, após assistido, informando a nota pessoal de um filme
- Remover um filme

b) index2.html – Filmes Populares

Página complementar dedicada à integração com a API externa TMDB e à manipulação de filmes populares salvos localmente.

Funcionalidades:
- Apresentar filmes populares buscado da API externa TMDB
- Adicionar filmes populares no banco 
- Atualizar informaçoes dos filmes como “adorei”  ❤️ ou  “quero assistir”👁️

c) Scripts JavaScript

Script : script.js  
Função : Controla a lógica da 'Minha Área' (`index.html`). Faz chamadas para a `minha_api` e`tmdb_api   

Script : scripts2.js
Função :Controla a página de 'Filmes Populares' (`index2.html`). Faz chamadas para a `filmespop_api` e `tmdb_api`. |

d) Rotas
A interface web (`meufront`) consome diretamente rotas HTTP utilizando JavaScript puro com `fetch`, garantindo a integração completa com os componentes back-end da aplicação.



# API Externa Utilizada

A aplicação faz uso da API externa gratuita 'The Movie Database (TMDB)' 
-  Site: https://developer.themoviedb.org  
-  Licença: Gratuita para uso educacional, pessoal e não comercial  
-  Cadastro: Foi necessário criar uma conta gratuita e gerar uma API Key , e neste projeto está sendo usado a conta criada pela aluna 
-  Rotas Utilizadas:
  - `GET /search/movie`: retorna dados de filmes com base em nome
  - `GET /movie/popular`: retorna lista de filmes populares

ATENÇÃO !! A chave de acesso à API TMDB (Bearer Token) foi enviada via plataforma da disciplina.  
Para funcionamento da aplicação, o professor deve inserir essa chave no arquivo `docker-compose.yml` no seguinte formato:

  tmdb_api:
    environment:
      - TMDB_API_KEY=sua_chave_aqui

# Rotas Implementadas

API Principal (`minha_api`)
- `GET /filmes`: Lista todos os filmes
- `GET /filme?nome_filme=...`: Busca um filme específico
- `POST /filme`: Adiciona novo filme
- `PUT /filme`: Atualiza nota pessoal ou status "assistido"
- `DELETE /filme?nome_filme=...`: Remove um filme

API Secundária (`filmespop_api`)
- `GET /filmespop`: Retorna filmes populares locais
- `POST /filmespop`: Adiciona novo filme popular
- `PUT /filmespop`: Atualiza filme popular
- `DELETE /filmespop?nome_filme=...`: Remove filme popular

API Intermediária (`tmdb_api`)
- `GET /nota?nome_filme=...`: Consulta a nota do filme no TMDB (API externa
- `GET /populares`: Consulta os filmes populares no TMDB (API externa)

Interface Web (`meufront`)
- Faz chamadas diretamente para todas as rotas REST(`GET`, `POST`, `PUT`, `DELETE`) via JavaScript
  - `index.html`: interage com `minha_api` e `tmdb_api`
  - `index2.html`: interage com `filmespop_api` e `tmdb_api`


## Banco de Dados

Cada componente de back-end possui seu próprio banco de dados PostgreSQL, criado e gerenciado automaticamente via containers Docker:

- `minha_api` utiliza o banco meubanco_minha_api
- `filmespop_api` utiliza o banco meubanco_filmespop_api


## Docker

Cada componente possui seu próprio `Dockerfile`. Todos são orquestrados via `docker-compose.yml` na raiz do projeto.

### Instruções de Execução com Docker compose:

a) Atualização manual da chave da token   **ATENÇÃO** 

Busque a chave da token da  API TMDB enviada pela plataforma da disciplina junto com a submissão do MVP, e incluia no docker-componser.yml

Inserir essa chave no arquivo `docker-compose.yml` no seguinte formato:

  tmdb_api:
    environment:
      - TMDB_API_KEY=**CHAVE INFORMADA PELA ALUNA NA PLATAFORMA**

a) Suba os containers
docker-compose -p my-movies up -d --build

