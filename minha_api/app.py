"""
  Projeto: My Movies
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC-Rio
  Data: Abril/2025
  Arquivo: app.py – API principal (minha_api - COMPONENTE Secundário)

  Descrição:
    Este arquivo define a API REST principal do projeto My Movies, desenvolvida com Flask e Flask-OpenAPI3.
    A API permite o cadastro, consulta, remoção e atualização de filmes, armazenados em um banco PostgreSQL.

    Funcionalidades:
      - Adição de filmes com dados fornecidos pelo usuário e nota do IMDb
      - Consulta de todos os filmes ou busca específica por nome
      - Atualização do status "Já assisti" e da nota pessoal do filme
      - Remoção de filmes pelo nome
      - Integração com documentação interativa via Swagger

    Esta API possui 5 rotas:
      - Rota GET    /filmes                   → lista todos os filmes cadastrados
      - Rota GET    /filme?nome_filme=...     → busca um filme específico
      - Rota POST   /filme                    → adiciona um novo filme ao banco
      - Rota PUT    /filme                    → atualiza nota ou status de um filme existente
      - Rota DELETE /filme?nome_filme=...     → remove um filme da base

    Esta API é consumida diretamente pela interface index.html (script.js) e compõe o backend principal do projeto.
"""

import os 
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, render_template, redirect, request, jsonify
from flask import redirect
from urllib.parse import unquote
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model import Session, Filme, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API para gerenciar cadastro de filmes do usuário", version="2.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
filme_tag = Tag(name="Filmes", description="Adição, alteração, consulta e remoção de filme à base")

"""
  Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
"""
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

"""
    Adiciona um novo Filme à base de dados
    Retorna uma representação dos filmes  .
"""
@app.post('/filme', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_filme(form: FilmeSchema):
    
    if form.minha_nota == "":
        form.minha_nota = None

    filme = Filme(
        nome_filme=form.nome_filme,
        genero=form.genero if hasattr(form, "genero") else None,
        nota_imdb =form.nota_imdb,
        ja_assisti = form.ja_assisti,
        minha_nota = form.minha_nota)
    logger.debug(f"Adicionando nome de filme: '{filme.nome_filme}'")
    
    try:
        session = Session()
        session.add(filme)
        session.commit()
        logger.debug(f"Adicionado nome de filme: '{filme.nome_filme}'")
        return apresenta_filme(filme), 200

    except IntegrityError as e:
        error_msg = "Filme de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar filme '{filme.nome_filme}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar filme '{filme.nome_filme}', {error_msg}")
        return {"message": error_msg}, 400


"""
    Faz a busca por todos os Filmes cadastrados
    Retorna uma representação da listagem de filmess.
"""
@app.get('/filmes', tags=[filme_tag],
         responses={"200": ListagemFilmesSchema, "404": ErrorSchema})
def get_filmes():

    logger.debug(f"Coletando filmes ")
    session = Session()
    filmes = session.query(Filme).all()

    if not filmes:
        return {"filmes": []}, 200
    else:
        logger.debug(f"%d filmesrodutos econtrados" % len(filmes))
        print(filmes)
        return apresenta_filmes(filmes), 200

"""
   Faz a busca por um Filme a partir do nome do filme
"""

@app.get('/filme', tags=[filme_tag],
         responses={"200": FilmeViewSchema, "404": ErrorSchema})

def get_filme(query: FilmeBuscaSchema):
    
    
    filme_nome = unquote(unquote(query.nome_filme))
    logger.debug(f"Coletando dados sobre filme '{filme_nome}'")
    
    session = Session()
    filme = session.query(Filme).filter(Filme.nome_filme == filme_nome).first()

    if not filme:
        error_msg = "Filme não encontrado na base :/"
        logger.warning(f"Erro ao buscar filme '{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404

    logger.debug(f"Filme encontrado: '{filme.nome_filme}'")
    return apresenta_filme(filme), 200

"""
   Deleta um Filme a partir do nome de filme informado
   Retorna uma mensagem de confirmação da remoção.
"""
@app.delete('/filme', tags=[filme_tag],
            responses={"200": FilmeDelSchema, "404": ErrorSchema})
def del_filme(query: FilmeBuscaSchema):
    filme_nome = unquote(unquote(query.nome_filme))
    print(filme_nome)
    logger.debug(f"Deletando dados sobre filme #{filme_nome}")
    session = Session()
    count = session.query(Filme).filter(Filme.nome_filme == filme_nome).delete()
    session.commit()

    if count:
        logger.debug(f"Deletado filme #{filme_nome}")
        return {"message": "Filme removido", "id": filme_nome}
    else:
        error_msg = "Filme não encontrado na base :/"
        logger.warning(f"Erro ao deletar filme #'{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404

"""
    Modifica as informações de Já Assiti e Nota do Filme na base de dados
    Retorna uma representação dos filmes associados.
"""
@app.put('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "404": ErrorSchema})
def update_filme(form: FilmeUpdateSchema):

    try:
        data = form.dict()
        session = Session()
        filme = session.query(Filme).filter(Filme.nome_filme == data['nome_filme']).first()
        if not filme:
            return jsonify({"message": "Filme não encontrado!"}), 404

        if 'ja_assisti' in data:
            filme.ja_assisti = data['ja_assisti']
        if 'minha_nota' in data:
            filme.minha_nota = data['minha_nota']

        session.commit()
        return jsonify({"message": "Filme atualizado com sucesso!", "filme": apresenta_filme(filme)}), 200

    except ValidationError as e:
        return jsonify({"message": "Erro de validação", "detalhes": e.errors()}), 422
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

