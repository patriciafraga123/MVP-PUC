"""
  Projeto: My Movies
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC-Rio
  Data: Abril/2025
  Arquivo: pop.py – API de Filmes Populares (API SEGUNDÁRIA)

  Descrição:
    Este arquivo define uma API secundária do projeto My Movies, desenvolvida com Flask e Flask-OpenAPI3.
    A API é responsável por armazenar e gerenciar localmente os filmes populares.
    Essa funcionalidade tem como objetivo otimizar o desempenho da aplicação, evitando chamadas repetidas ao serviço externo,
    além de permitir ao usuário marcar quais filmes ele adorou e/ou deseja assistir futuramente.

  Funcionalidades:
    - Armazenamento em lote no banco de dados de filmes populares obtidos da API TMDb_api
    - Cadastro manual de um filme popular individual
    - Consulta de todos os filmes populares armazenados no banco
    - Atualização dos campos "adorei" e "watchlist" para filmes populares já cadastrados

  Esta API possui 4 rotas:
    - Rota POST   /salvar-filmes     → salva no banco em lote os filmes populares recebidos (ignora duplicados)
    - Rota GET    /filmespop         → retorna todos os filmes populares armazenados no banco
    - Rota POST   /salvar-filme      → salva manualmente um filme popular individual no banco
    - Rota PUT    /atualizar-filme   → atualiza os campos "adorei" ou "watchlist" de um filme popular existente

  Esta API é consumida diretamente pela interface index2.html (script2.js) e compõe o backend secundário do projeto.
"""

import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, request, jsonify, redirect
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model import FilmePop, Session
from pydantic import ValidationError
from schemas import FilmePopSchema, FilmeUpdateSchema
from typing import List
from flask_cors import CORS

info = Info(title="API para gerenciar cadastro de Filmes Polulares", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
filmepop_tag = Tag(name="Filmes Populares", description="Adição, alteração, consulta e remoção de filme populares à base")

"""
  Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
"""
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


"""
 Rota Post - Salva em lote uma lista de filmes populares na base de dados, ignorando os que já existem.

"""
@app.post('/salvar-filmes', tags=[filmepop_tag])
def salvar_filmes():
    session = Session()
    try:
        filmes_recebidos = request.json
        print("Filmes recebidos:", filmes_recebidos)
        salvos = 0
        ignorados = 0

        for filme in filmes_recebidos:
            # Verifica se o filme já existe pelo ID
            existe = session.query(FilmePop).filter(
                FilmePop.filme_pop_id == filme['id']
            ).first()

            if existe:
                ignorados += 1
                continue

            novo_filme = FilmePop(
                filme_pop_id=filme['id'],
                nome_filme_pop=filme['original_title'],
                img_pop=filme['poster_path'],
                nota_pop=filme['vote_average'],
                adorei_pop=" ",
                watchlist_pop="Não"
            )
            session.add(novo_filme)
            salvos += 1

        session.commit()
        return jsonify({
            "message": f"{salvos} filmes salvos com sucesso. {ignorados} já existiam e foram ignorados."
        }), 201

    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Erro ao inserir filmes"}), 400
    finally:
        session.close()

"""
    Rota Get - Retorna a lista de filmes populares armazenados no banco de dados.

"""
@app.get('/filmespop', tags=[filmepop_tag])
def listar_filmes():
    session = Session()
    try:
        #filmes = session.query(FilmePop).all()
        filmes = session.query(FilmePop).order_by(FilmePop.filme_pop_id.asc()).all()

        filmes_json = [{
            "id": filme.filme_pop_id,
            "nome": filme.nome_filme_pop,
            "imagem": filme.img_pop,
            "nota": filme.nota_pop,
            "adorei": filme.adorei_pop,
            "watchlist": filme.watchlist_pop
        } for filme in filmes]

        return jsonify(filmes_json), 200
    finally:
        session.close()

"""
    Rota Post - adiciona um novo filme popular no banco de dados
"""


@app.post('/salvar-filme', tags=[filmepop_tag])
def salvar_filme(form: FilmePopSchema):
    session = Session()
    try:
        novo_filme = FilmePop(
            filme_pop_id=form.filme_pop_id,
            nome_filme_pop=form.nome_filme_pop,
            img_pop=form.img_pop,
            nota_pop=form.nota_pop,
            adorei_pop=form.adorei_pop or '',
            watchlist_pop=form.watchlist_pop or 'Não'
        )

        session.add(novo_filme)
        session.commit()

        return jsonify({"message": "Filme salvo com sucesso"}), 201

    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Erro ao inserir filme, possível ID duplicado"}), 400
    finally:
        session.close()

        
"""
    Rota PUT - Atualiza o status "adorei" ou "watchlist" no banco de um filme já salvo
"""

@app.put('/atualizar-filme', tags=[filmepop_tag])
def atualizar_filme(form: FilmeUpdateSchema):
    session = Session()
    try:
        filme = session.query(FilmePop).filter(FilmePop.filme_pop_id == form.filme_pop_id).first()

        if not filme:
            return jsonify({"error": "Filme não encontrado"}), 404

        if form.adorei_pop is not None:
            filme.adorei_pop = form.adorei_pop
        if form.watchlist_pop is not None:
            filme.watchlist_pop = form.watchlist_pop

        session.commit()
        return jsonify({"message": "Filme atualizado com sucesso"}), 200

    except ValidationError as e:
        return jsonify({"message": "Erro de validação", "detalhes": e.errors()}), 422

    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

    finally:
        session.close()

# Inicia a aplicação Flask na porta 5002
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
