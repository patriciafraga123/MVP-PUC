// Lista global para armazenar os filmes já cadastrados
let filmesCadastrados = [];

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
    let url = 'http://127.0.0.1:5000/filmes';
    fetch(url, {
        method: 'get',
    })
        .then((response) => response.json())
        .then((data) => {

            for (const item of data.filmes) {
                // Insere os filmes nas tabelas
                insertList(item.nome_filme, item.genero, item.nota_imdb, item.ja_assisti, item.minha_nota);
                insertList2(item.nome_filme, item.genero, item.nota_imdb, item.ja_assisti, item.minha_nota);

                // Adiciona o nome do filme à lista global
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
  Função para colocar um item na lista do servidor via requisição POST
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


    let url = 'http://127.0.0.1:5000/filme';
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
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
    let close = document.getElementsByClassName("close");
    let i;
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            let div = this.parentElement.parentElement;
            const nomeItem = div.getElementsByTagName('td')[0].innerHTML
            if (confirm("Você tem certeza?")) {
                div.remove()
                deleteItem(nomeItem)
                alert("Removido!")
            }
        }
    }
}


/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
    console.log(item)
    let url = 'http://127.0.0.1:5000/filme?nome_filme=' + item;
    fetch(url, {
        method: 'delete'
    })
        .then((response) => response.json())
        .catch((error) => {
            console.error('Error:', error);
        });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo filme
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
    let inputFilme = document.getElementById("newInput").value;
    let inputGenero = document.getElementById("newGenero").value;
    let inputIMDB = document.getElementById("newIMDB").value;
    let inputAssisti = document.getElementById("newAssisti").value;
    let inputNota = document.getElementById("newNota").value;

    // Normaliza o nome do filme para comparação
    let normalizedFilme = inputFilme.trim().toLowerCase();

    console.log("Filmes cadastrados:", filmesCadastrados); // Verificacao
    console.log("Tentando adicionar:", inputFilme); // Verificacao

    // Validação: Nome do filme não pode estar vazio
    if (inputFilme === '') {
        alert("Inclua o nome do filme!");
        return;
    }
    // Validação: Verifica se o filme já está na lista
    if (filmesCadastrados.includes(normalizedFilme)) {
        alert("Este filme já está cadastrado!");
        return;
    }

    // Validação: Gênero deve estar preenchido
    if (inputGenero.trim() === '') {
        alert("Preencha o gênero do filme!");
        return;
    }

    // Validação: Campo 'Assisti' deve estar preenchido
    if (inputAssisti.trim() === '') {
        alert("Informe se você já assistiu ao filme!");
        return;
    }

    // Validação: IMDB e Nota devem ser números
    if (isNaN(Number(inputIMDB)) || isNaN(Number(inputNota))) {
        alert("Notas precisam ser números!");
        return;
    }

    // Validação: Se 'Assisti' for 'Sim', 'Nota' deve estar preenchida
    if (inputAssisti.toLowerCase() === 'sim' && inputNota.trim() === '') {
        alert("Se você já assistiu ao filme, a nota precisa ser preenchida!");
        return;
    }

    // Validação: Se 'Assisti' for diferente de 'Sim', 'Nota' não pode estar preenchida
    if (inputAssisti.toLowerCase() !== 'sim' && inputNota.trim() !== '') {
        alert("Se você ainda não assistiu ao filme, a nota não deve ser preenchida!");
        return;
    }

    // Se todas as validações passarem, adiciona o item
    insertList(inputFilme, inputGenero, inputIMDB, inputAssisti, inputNota);
    insertList2(inputFilme, inputGenero, inputIMDB, inputAssisti, inputNota);
    postItem(inputFilme, inputGenero, inputIMDB, inputAssisti, inputNota);
    // Atualiza a lista global de filmes cadastrados
    filmesCadastrados.push(normalizedFilme);
    alert("Item adicionado!");
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista 1 apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameFilme, genero, imdb, assisti, nota) => {
    if (assisti !== "Sim") {
        return; // Se não for "Sim", sai da função sem inserir
    }
    // let item = [nameFilme, genero, imdb, assisti, nota]
    let item = [nameFilme, genero, imdb, nota]
    let table = document.getElementById('myTable');
    let row = table.insertRow();

    for (let i = 0; i < item.length; i++) {
        let cel = row.insertCell(i);
        cel.textContent = item[i];
    }
    insertButton(row.insertCell(-1))
    document.getElementById("newInput").value = "";
    document.getElementById("newGenero").value = "";
    document.getElementById("newIMDB").value = "";
    // document.getElementById("newAssisti").value = "";
    document.getElementById("newNota").value = "";

    removeElement()
}



/*
  --------------------------------------------------------------------------------------
  @@ Codigo Novo - Função para inserir e editar items na lista 2 apresentada
  --------------------------------------------------------------------------------------
*/
// Função para atualizar os dados do filme no backend

const updateItem = async (nomeFilmeAntigo, assisti, nota) => {
    const formData = new FormData();
    formData.append('nome_filme', nomeFilmeAntigo);
    formData.append('ja_assisti', assisti);
    formData.append('minha_nota', assisti === "Sim" ? (nota.trim() !== "" ? nota : null) : null); // Nota como string

    let url = 'http://127.0.0.1:5000/filme';
    try {
        const response = await fetch(url, {
            method: 'PUT',
            body: formData // Usando FormData
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
}
// Funça para limpar os dados inputados
const limparCampos = () => {
    document.getElementById("newInput").value = "";
    document.getElementById("newGenero").value = "";
    document.getElementById("newIMDB").value = "";
    document.getElementById("newNota").value = "";
};

// Função para inserir um novo filme na tabela
const insertList2 = (nameFilme, genero, imdb, assisti, nota) => {
    if (assisti !== "Não") {
        return; // Só insere filmes que ainda não foram assistidos
    }

    let item = [nameFilme, genero, imdb, assisti, nota];
    let table = document.getElementById('myTable2');
    let row = table.insertRow();

    // Adiciona os dados de cada coluna
    for (let i = 0; i < item.length; i++) {
        let cel = row.insertCell(i);
        cel.textContent = item[i];
    }

    // Botão de deletar
    insertButton(row.insertCell(-1));

    // Botão de atualizar
    let updateCell = row.insertCell(-1);
    let updateButton = document.createElement("button");
    updateButton.textContent = "Update";

    updateButton.onclick = () => {
        let assistiCell = row.cells[3];
        let notaCell = row.cells[4];

        let assistiInput = document.createElement("input");
        assistiInput.type = "text";
        assistiInput.value = assistiCell.textContent;

        let notaInput = document.createElement("input");
        notaInput.type = "text";
        notaInput.value = notaCell.textContent;

        assistiCell.textContent = "";
        assistiCell.appendChild(assistiInput);

        notaCell.textContent = "";
        notaCell.appendChild(notaInput);

        updateButton.textContent = "Salvar";
        updateButton.onclick = () => {
            let assistiValue = assistiInput.value.trim();
            if (assistiValue !== "Sim" && assistiValue !== "Não") {
                alert("O campo 'Assisti' deve ser 'Sim' ou 'Não'.");
                return;
            }

            let notaValue = parseInt(notaInput.value, 10);
            if (assistiValue === "Sim" && (isNaN(notaValue) || notaValue < 0 || notaValue > 10)) {
                alert("A nota deve ser um número inteiro entre 0 e 10 se o filme foi assistido.");
                return;
            }

            assistiCell.textContent = assistiValue;
            notaCell.textContent = assistiValue === "Sim" ? notaValue : "";

            updateItem(row.cells[0].textContent, assistiValue, notaInput.value);

            updateButton.textContent = "Update";
            updateButton.onclick = () => {
                // Repetir lógica de edição
            };
        };
    };

    updateCell.appendChild(updateButton);

    // Limpa os campos de entrada
    limparCampos();

    // Atualiza os eventos de remoção
    removeElement();
};