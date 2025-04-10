# meufront – Interface Web do Projeto My Movies  *(COMPONENTE PRINCIPAL)*

Este componente fornece a interface do usuário para o projeto My Movies. Construída com HTML, CSS e JavaScript puro, permite ao usuário interagir com as APIs do projeto de forma intuitiva e funcional.

## Funcionalidades

A aplicação web possui duas páginas principais:

###  `index.html` – Minha Lista Pessoal
Permite:
- Adicionar um novo filme à lista pessoal
- Visualizar todos os filmes cadastrados
- Atualizar um filme com nota pessoal após assistido
- Remover filmes da lista

### `index2.html` – Filmes Populares
Permite:
- Buscar filmes populares da API externa TMDB
- Salvar filmes populares no banco local
- Marcar filmes como "quero assistir" 👁️ ou "adorei" ❤️

### JavaScript
- `script.js`: Lida com a lógica de `index.html`, interagindo com `minha_api` e `tmdb_api`.
- `scripts2.js`: Lida com a lógica de `index2.html`, interagindo com `filmespop_api` e `tmdb_api`.

## Integração com APIs e Critério de Avaliação

A interface web (`meufront`) foi desenvolvida com JavaScript puro, utilizando `fetch` para fazer chamadas diretas às rotas HTTP das APIs do projeto.

### Chamadas Realizadas pelo Front-End

#### `index.html` – Minha Lista Pessoal

Integra com:
- `minha_api` (filmes pessoais)
- `tmdb_api` (dados vindos da API pública TMDB)

Rotas chamadas:
- `GET /filmes` – listar todos os filmes cadastrados  
- `POST /filme` – adicionar novo filme pessoal  
- `PUT /filme` – atualizar nota pessoal ou status "assistido"  
- `DELETE /filme?nome_filme=...` – remover filme da lista pessoal  
- `GET /nota?nome_filme=...` – buscar nota do filme na API TMDB  

#### `index2.html` – Filmes Populares

Integra com:
- `filmespop_api` (filmes populares locais)
- `tmdb_api` (dados vindos da API pública TMDB)

Rotas chamadas:
- `GET /filmespop` – buscar lista de filmes populares armazenados no banco de dados  
- `POST /salvar-filmes` – adicionar filmes populares ao banco local  
- `PUT /atualizar-filme` – atualizar marcações (❤️ “adorei”, 👁️ “quero assistir”)  
- `GET /populares` – buscar filmes populares da API externa TMDB  

## Estrutura do Projeto

Pasta `meufront/`:

- `images/` — Imagens usadas no front
- `index.html` — Página principal (My Area)
- `index2.html` — Página de filmes populares (Most Popular Movies)
- `script.js` — JS da index.html (minha lista)
- `scripts2.js` — JS da index2.html (filmes populares)
- `style.css` — Estilo das páginas (usado em ambas as páginas)
- `README.md` — Instruções específicas deste componente
- `READMEGERAL.md` — Instruções gerais da aplicação



## Integração com o Backend

Este frontend atua como gateway entre o usuário e os seguintes componentes:

- `tmdb_api` (porta 5001): responsável por buscar filmes da API externa TMDb
- `filmespop_api` (porta 5002): responsável por armazenar e atualizar os filmes populares no banco local

### Fluxo na Página de Filmes Populares (`index2.html`)

1. A função `getList()` é executada automaticamente ao carregar a página:
   - Busca os filmes da rota `GET /populares` da `tmdb_api`
   - Salva esses filmes localmente via `POST /salvar-filmes` da `filmespop_api`
   - Exibe os filmes salvos com notas e botões interativos

2. Ao clicar em ❤️ ou 👁️:
   - A função `enviarAtualizacaoFilme()` atualiza o banco usando a rota `PUT /atualizar-filme`

3. A lista de filmes salvos é carregada com `GET /filmespop`

## Tecnologias Utilizadas

- HTML5
- CSS3
- JavaScript Puro
- API Fetch
- Integração com Flask (via `fetch`)

## Executando com Docker Compose

O arquivo `docker-compose.yml` está localizado na **raiz do meufront** (componente principal).

Passos para executar usando o Docker Composer:

1. Certifique-se de que o Docker esteja instalado e em execução.
2. Na raiz do folder meufront, edite o arquivo `docker-compose.yml` para atualizar que a chave `TMDB_API_KEY` que foi informada pela aluna na plataforma da disciplina   *** ATENÇÃO ****
3. No terminal, execute:
docker-compose -p my-movies up -d --build
