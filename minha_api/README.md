Minha API de Filmes

Este projeto faz parte do MVP de Patricia Fraga da Disciplina Desenvolvimento Full Stack Básico
que tem o objetivo de permitir que os usuários insiram informações sobre filmes que desejam assistir ou já assistiram, como título, gênero, avaliação no IMDb, status de visualização ("Assisti" ou "Não") e uma nota pessoal. Além disso, é possível editar de campos de status de visualização e nota, garantindo flexibilidade e controle sobre os dados inseridos.


Como executar

Será necessário ter todas as libs python listadas no requirements.txt instaladas. Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

python3 -m venv env
source env/bin/activate

  É fortemente indicado o uso de ambientes virtuais do tipo virtualenv.

Estes comandos instalam as dependências/bibliotecas, descritas no arquivo requirements.txt.

(env)$ pip install --upgrade pip
(env)$ pip install -r requirements.txt

Para executar a API basta executar:

(env)$ flask run --host 0.0.0.0 --port 5000


Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

(env)$ flask run --host 0.0.0.0 --port 5000 --reload

Abra o http://localhost:5000/#/ no navegador para verificar o status da API em execução.
