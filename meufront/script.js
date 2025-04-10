
/*
  Projeto: My Movies
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC RJ
  Data: Abril/2025
  Arquivo: script.js – Script JavaScript de interação com a interface index.html

  Descrição:
    Define a lógica de funcionamento da interface da página "My Area" (index.html),
    funcionando como um gateway entre a interface do usuário e as APIs do backend:
      - minha_api (app.py)/5000: API principal para gerenciamento do banco de filmes
      - tmdb_api (tmdb.py)/5001: API intermediária para busca de notas no serviço externo TMDb

    Através desse script, a interface permite:
      - Cadastrar filmes já assistidos e os que desejam assistir
      - Exibir listas de filmes assistidos e para assistir
      - Adicionar, atualizar, buscar e remover filmes do banco de dados
      - Obter automaticamente a nota TMDb de um filme via API externa
      - Realizar validações básicas antes do envio de dados

    Os filmes cadastrados são organizados em duas listas distintas na interface:
      - "My Ratings": filmes assistidos e avaliados
      - "My Watchlist": filmes que desejo assistir

    Toda a interação com o backend é feita por meio de requisições assíncronas (fetch).
*/

// Lista global para armazenar os filmes já cadastrados
let filmesCadastrados = [];

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de filmes do usuário gravados no banco via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
    let url = 'http://localhost:5000/filmes';
    fetch(url, {
        method: 'get',
    })
        .then((response) => response.json())
        .then((data) => {

            for (const item of data.filmes) {
                // Insere os filmes nas tabelas
                insertList(item.nome_filme, item.genero, item.nota_imdb, item.ja_assisti, item.minha_nota);
                insertList2(item.nome_filme, item.nota_imdb, item.ja_assisti, item.minha_nota);
                filmesCadastrados.push(item.nome_filme.trim().toLowerCase());
            }

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um filme no banco via requisição POST
  --------------------------------------------------------------------------------------
*/

const postItem = async (inputFilme, inputGenero, inputIMDB, inputAssisti, inputNota) => {
    const formData = new FormData();
    formData.append('nome_filme', inputFilme);
    formData.append('genero', inputGenero);
    formData.append('nota_imdb', inputIMDB);
    formData.append('ja_assisti', inputAssisti);

    if (inputNota.trim() !== "") {
        formData.append('minha_nota', parseInt(inputNota, 10));
    }


    let url = 'http://localhost:5000/filme';
    fetch(url, {
        method: 'post',
        body: formData
    })
        .then((response) => response.json())
        .catch((error) => {
            console.error('Error:', error);
        });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/

const insertButton = (parent) => {
    let button = document.createElement("button");
    button.innerHTML = "🗑️";
    button.className = "delete-btn";
    button.setAttribute("aria-label", "Remover filme");
    parent.appendChild(button);
};


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
    let buttons = document.getElementsByClassName("delete-btn");
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].onclick = null;

        buttons[i].onclick = function () {
            const row = this.closest("tr");


            if (!row || row.cells.length === 0) {
                console.warn("Linha da tabela não encontrada ou sem células.");
                return;
            }

            const nomeItem = row.cells[0].textContent.trim();
            const normalizedNome = nomeItem.toLowerCase();

            if (confirm("Você tem certeza?")) {
                row.remove();
                deleteItem(nomeItem);

                const index = filmesCadastrados.indexOf(normalizedNome);
                if (index > -1) {
                    filmesCadastrados.splice(index, 1);
                }

                alert("Removido!");
            }
        };
    }
};


/*
  --------------------------------------------------------------------------------------
  Função para buscar nota do filme na API tmdb.py que conecta com uma API externa
  --------------------------------------------------------------------------------------
*/
const buscaNota = async (item) => {
    console.log(item);
    let url = 'http://localhost:5001/nota?nome_filme=' + item;

    try {

        const response = await fetch(url, { method: 'get' });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data.nota;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
};


/*
  --------------------------------------------------------------------------------------
  Função para deletar um filme do banco via requisição DELETE
  --------------------------------------------------------------------------------------
*/

const deleteItem = (item) => {
    const encodedItem = encodeURIComponent(item);
    let url = 'http://localhost:5000/filme?nome_filme=' + encodedItem;

    fetch(url, {
        method: 'delete'
    })
        .then((response) => response.json())
        .catch((error) => {
            console.error('Error:', error);
        });
};
/*
  --------------------------------------------------------------------------------------
// Função que adiciona um novo filme após validar os dados e buscar a nota na API
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
    let inputFilme = document.getElementById("newInput").value;
    let inputGenero = "";
    let inputIMDB = "";
    let inputAssisti = document.getElementById("newAssisti").value;
    let inputNota = document.getElementById("newNota").value;

    let normalizedFilme = inputFilme.trim().toLowerCase();

    try {
        let notafilme = await buscaNota(inputFilme);
        inputIMDB = parseFloat(notafilme);

        if (inputFilme === '') {
            alert("Inclua o nome do filme!");
            return;
        }

        if (filmesCadastrados.includes(normalizedFilme)) {
            alert("Este filme já está cadastrado!");
            return;
        }

        if (inputAssisti.trim() === '') {
            alert("Informe se você já assistiu ao filme!");
            return;
        }


        if (inputAssisti === 'Sim') {
            let nota = parseFloat(inputNota);
            if (isNaN(nota) || nota < 0 || nota > 10) {
                alert("Nota precisa ser um número entre 0 e 10!");
                return;
            }
        }


        if (inputAssisti === 'Não' && inputNota.trim() !== '') {
            alert("Se você ainda não assistiu ao filme, a nota não deve ser preenchida!");
            return;
        }

        insertList(inputFilme, inputGenero, inputIMDB, inputAssisti, inputNota);
        insertList2(inputFilme, inputIMDB, inputAssisti, inputNota);
        postItem(inputFilme, inputGenero, inputIMDB, inputAssisti, inputNota);
        filmesCadastrados.push(normalizedFilme);
        alert("Item adicionado!");
        limparCampos();
    } catch (error) {
        console.error('Erro ao obter a nota:', error);
    }
};

/*
  --------------------------------------------------------------------------------------
  Função para inserir filmes na lista My ratings
  --------------------------------------------------------------------------------------
*/
const insertList = (nameFilme, genero, imdb, assisti, nota) => {
    if (assisti !== "Sim") {
        return;
    }

    let imdbFormatado = imdb ? parseFloat(imdb).toFixed(1) : "";
    let notaFormatada = nota ? parseFloat(nota).toFixed(1) : "";

    let item = [nameFilme, imdbFormatado, notaFormatada];
    let table = document.getElementById('myTable');
    let row = table.insertRow();

    for (let i = 0; i < item.length; i++) {
        let cel = row.insertCell(i);
        cel.textContent = item[i];
    }

    insertButton(row.insertCell(-1));

    document.getElementById("newInput").value = "";
    document.getElementById("newNota").value = "";


    removeElement();
};

/*
  --------------------------------------------------------------------------------------
  Função para atualizar no banco a nota do filme via requisição PUT
  --------------------------------------------------------------------------------------
*/

const updateItem = async (nomeFilmeAntigo, assisti, nota) => {
    const formData = new FormData();
    formData.append('nome_filme', nomeFilmeAntigo);
    formData.append('ja_assisti', 'Sim');
    formData.append('minha_nota', nota);

    let url = 'http://localhost:5000/filme';
    try {
        const response = await fetch(url, {
            method: 'PUT',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            console.log('Filme atualizado:', result);
        } else {
            console.error('Erro ao atualizar filme:', result.message);
        }
    } catch (error) {
        console.error('Erro ao atualizar filme:', error);
    }
};

// Função para limpar os dados inputados
const limparCampos = () => {
    document.getElementById("newInput").value = "";

    document.getElementById("newNota").value = "";
};

// Função para inserir um novo filme na tabela My Watchlist

const insertList2 = (nameFilme, imdb, assisti, nota) => {
    if (assisti !== "Não") return;

    let table = document.getElementById('myTable2');
    let row = table.insertRow();

    // Formatar notas com uma casa decimal
    let imdbFormatado = parseFloat(imdb).toFixed(1);
    let notaFormatada = nota ? parseFloat(nota).toFixed(1) : "";

    // Inserir nome do filme, nota do IMDB e nota do usuário
    let item = [nameFilme, imdbFormatado, notaFormatada];
    for (let i = 0; i < item.length; i++) {
        let cel = row.insertCell(i);
        cel.textContent = item[i];
    }

    // Célula para os botões de ação
    let actionCell = row.insertCell(-1);
    let iconWrapper = document.createElement("div");
    iconWrapper.className = "action-icons";

    // 🗑️ Botão de deletar
    let deleteButton = document.createElement("button");
    deleteButton.innerHTML = "🗑️";
    deleteButton.className = "delete-btn";
    deleteButton.setAttribute("aria-label", "Remover filme");

    deleteButton.onclick = function () {
        const row = this.closest("tr");
        const nomeItem = row.cells[0].textContent.trim();
        const normalizedNome = nomeItem.toLowerCase();

        if (confirm("Você tem certeza?")) {
            row.remove();
            deleteItem(nomeItem);

            const index = filmesCadastrados.indexOf(normalizedNome);
            if (index > -1) {
                filmesCadastrados.splice(index, 1);
            }

            alert("Removido!");
        }
    };

    iconWrapper.appendChild(deleteButton);

    let editButton = document.createElement("button");
    editButton.innerHTML = "✏️";
    editButton.className = "icon-btn";
    editButton.setAttribute("aria-label", "Editar nota");

    editButton.onclick = async function () {
        const rating = prompt("Qual a sua nota para este filme (0-10)?");
        const notaNumerica = parseFloat(rating);

        if (isNaN(notaNumerica) || notaNumerica < 0 || notaNumerica > 10) {
            alert("Nota inválida! Use um número entre 0 e 10.");
            return;
        }

        await updateItem(nameFilme, "Sim", notaNumerica);

        row.remove();
        insertList(nameFilme, "", imdb, "Sim", notaNumerica);
        removeElement();
        alert("Filme atualizado com sucesso!");
    };
    iconWrapper.appendChild(editButton);

    actionCell.appendChild(iconWrapper);

    removeElement();

};

