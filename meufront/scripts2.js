/*
  Projeto: My Movies
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC RJ
  Data: Abril/2025
  Arquivo: scripts2.js – Script JavaScript de interação com a interface index2.html

  Descrição:
    Define a lógica de funcionamento da interface da página "Most Popular Movies" (index2.html),
    funcionando como um gateway entre a interface do usuário e as APIs do backend:
      - filmespop_api (pop.py)/5002: API secundária para gerenciamento e atualização dos filmes populares no banco
      - tmdb_api (tmdb.py)/5001: API intermediária para busca de dados no serviço externo TMDb

    Através desse script, a interface permite:
      - Buscar filmes populares da API externa via backend
      - Armazenar e atualizar informações dos filmes populares no banco de dados
      - Exibir os filmes como cards interativos com nota TMDb
      - Marcar filmes como "Adorei" ou "Watchlist", com persistência no banco

*/


/*
  --------------------------------------------------------------------------------------
  Função que inicializa a página buscando os filmes populares, salvando no banco e exibindo na tela
  --------------------------------------------------------------------------------------
*/

const getList = async () => {
    const url = 'http://localhost:5001/populares';

    try {
        const response = await fetch(url);
        const data = await response.json();

        console.log("Filmes recebidos da API local:", data);

        await salvarFilmesNoBanco(data);

        await carregarFilmesDoBanco();

    } catch (err) {
        console.error("Erro ao buscar filmes da API local:", err);
    }
};


/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/

getList()

/*
  --------------------------------------------------------------------------------------
  Função para apresentar lista de filmes populares na tela 
  --------------------------------------------------------------------------------------
*/
const insertCard = (filme) => {
    console.log("Renderizando filme:", filme);
    const section = document.getElementById('filmes-list');
    const article = document.createElement('article');
    article.setAttribute('class', 'filme');
    article.setAttribute('id', filme.id);

    // Imagem do filme
    const img = document.createElement('img');
    img.setAttribute('src', `https://image.tmdb.org/t/p/w500${filme.imagem}`);
    img.setAttribute('alt', 'Não foi possível carregar a imagem do filme');

    // Título do filme
    const p = document.createElement('p');
    p.setAttribute('class', 'name-filme');
    p.innerHTML = filme.nome;

    // Nota
    const h3 = document.createElement('h3');
    h3.setAttribute('class', 'rating-filme');
    const span = document.createElement('span');
    span.innerHTML = 'TMDB Rating: ' + filme.nota.toFixed(1);
    h3.appendChild(span);

    // Container de botões (❤️ e 👁️)
    const botoesContainer = document.createElement('div');
    botoesContainer.classList.add('botoes-filme');

    // Botão Adorei ❤️
    const adoreiBtn = document.createElement('button');
    adoreiBtn.classList.add('btn-icon', 'btn-adorei');
    adoreiBtn.innerHTML = '❤️';

    // Botão Watchlist 👁️
    const watchlistBtn = document.createElement('button');
    watchlistBtn.classList.add('btn-icon', 'btn-watchlist');
    watchlistBtn.innerHTML = '👁️';


    if (filme.adorei === "Sim") {
        adoreiBtn.classList.add('selecionado');
    }
    if (filme.watchlist === "Sim") {
        watchlistBtn.classList.add('selecionado');
    }

    // Eventos dos botões
    adoreiBtn.addEventListener('click', () => {
        adoreiBtn.classList.toggle('selecionado');
        const adoreiSelecionado = adoreiBtn.classList.contains('selecionado');
        const watchlistSelecionado = watchlistBtn.classList.contains('selecionado');
        enviarAtualizacaoFilme(filme.id, adoreiSelecionado, watchlistSelecionado);
    });

    watchlistBtn.addEventListener('click', () => {
        watchlistBtn.classList.toggle('selecionado');
        const adoreiSelecionado = adoreiBtn.classList.contains('selecionado');
        const watchlistSelecionado = watchlistBtn.classList.contains('selecionado');
        enviarAtualizacaoFilme(filme.id, adoreiSelecionado, watchlistSelecionado);
    });

    // Adiciona os botões ao container
    botoesContainer.appendChild(adoreiBtn);
    botoesContainer.appendChild(watchlistBtn);

    // Monta o card final
    article.appendChild(img);
    article.appendChild(p);
    article.appendChild(h3);
    article.appendChild(botoesContainer);
    section.appendChild(article);
};

/*
  --------------------------------------------------------------------------------------
  Função para chamar o backend para inserir filmes populares no banco 
  --------------------------------------------------------------------------------------
*/

const salvarFilmesNoBanco = async (filmes) => {
    let url = 'http://localhost:5002/salvar-filmes';

    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filmes)
    };

    try {
        const response = await fetch(url, options);
        const result = await response.json();

        if (response.ok) {
            console.log("Filmes salvos com sucesso:", result);
        } else {
            console.error("Erro ao salvar filmes:", result.message);
        }

    } catch (error) {
        console.error("Erro na requisição:", error);
    }
};

/*
  --------------------------------------------------------------------------------------
  Função para chamar atualizar no banco as informacoes de 'adorei'e 'watchlist' 
  --------------------------------------------------------------------------------------
*/

const enviarAtualizacaoFilme = async (id, adorei, watchlist) => {
    const url = 'http://localhost:5002/atualizar-filme';

    // Criando o FormData em vez de JSON
    const formData = new FormData();
    formData.append("filme_pop_id", id);
    formData.append("adorei_pop", adorei ? "Sim" : "Não");
    formData.append("watchlist_pop", watchlist ? "Sim" : "Não");

    try {
        const response = await fetch(url, {
            method: 'PUT',
            body: formData, // Envia como multipart/form-data
        });

        const result = await response.json();

        if (response.ok) {
            console.log("Filme atualizado com sucesso:", result);
        } else {
            console.error("Erro ao atualizar filme:", result);
        }

    } catch (error) {
        console.error("Erro na requisição:", error);
    }
};


/*
  --------------------------------------------------------------------------------------
   Função para buscar todos os filmes salvos no banco de dados
    e exibir esses filmes na tela 
--------------------------------------------------------------------------------------
*/
const carregarFilmesDoBanco = async () => {
    let url = 'http://localhost:5002/filmespop';

    try {
        const response = await fetch(url);
        const filmes = await response.json();

        console.log("Filmes recebidos do banco:", filmes);

        if (Array.isArray(filmes)) {
            document.getElementById('filmes-list').innerHTML = '';
            filmes.forEach(insertCard);
        } else {
            console.error("Resposta inesperada do backend:", filmes);
        }

    } catch (error) {
        console.error("Erro ao carregar filmes do banco:", error);
    }
};
