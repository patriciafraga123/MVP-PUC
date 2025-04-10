"""
  Projeto: My Movies
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC-Rio
  Data: Abril/2025
  Arquivo: tmdb.py – Essa API é um componente integrador para conectar com  API externa do TBMD

  Descrição:
    Este arquivo define a API intermediária que realiza consultas à plataforma The Movie Database (TMDB).
    Desenvolvida com Flask e Flask-OpenAPI3, essa API permite a obtenção de dados externos para enriquecer
    as funcionalidades do sistema, como a nota dos filmes e a listagem de filmes populares.

    API Externa Utilizada:
      - Nome: TMDB (The Movie Database)
      - URL base: https://api.themoviedb.org/3
      - Licença: Uso gratuito mediante cadastro
      - Requisitos: Necessário obter uma API Key pessoal (configurada como variável de ambiente TMDB_API_KEY)

    Endpoints da TMDB utilizados nesta aplicação:
      1. /search/movie    → utilizado para buscar e retornar a nota de um filme
      2. /movie/popular   → utilizado para obter a lista atualizada de filmes populares

    Esta API fornece 2 rotas principais:
      - Rota GET /nota        → Consulta à nota de um filme no TMDB (via /search/movie)
      - Rota GET /populares   → Consulta à lista de filmes populares (via /movie/popular)

   
"""

import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, jsonify, redirect, request
import requests
from flask_cors import CORS
from pydantic import BaseModel

info = Info(title="API para consultar APIs externas TMDB", version="1.0.0")
tmdb = OpenAPI(__name__, info=info)  
CORS(tmdb)  

home_tag = Tag(name="Documentação API externa TMDB", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
nota_tag = Tag(name="Nota filme", description="Busca a nota de um filme")
populares_tag = Tag(name="Consulta Filmes Populares", description="Busca os filmes populares usando a API externa TMDB")

"""
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
"""
@tmdb.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

class NotaQueryParams(BaseModel):
    nome_filme: str

"""
    Obtém a nota de um filme a partir do The Movie Database (TMDB)
"""
@tmdb.get('/nota', tags=[nota_tag])    
def obter_nota(query: NotaQueryParams):
    
    nome_filme = query.nome_filme 
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        return {"error": "API Key não configurada no ambiente."}, 500

    url = f"https://api.themoviedb.org/3/search/movie?query={nome_filme}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json", 
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            resultado = data['results'][0]
            return {"nome_filme": nome_filme, "nota": resultado.get('vote_average', 'Não disponível')}
    return {"error": "Filme não encontrado"}

"""
    Obtém lista de filmes populares do TMDB
        
"""
@tmdb.get('/populares', tags=[populares_tag])    
def filmes_populares():
 
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        return {"error": "API Key não configurada."}, 500

    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    
    return {"error": "Erro ao consultar TMDB"}

if __name__ == '__main__':
  
    # Iniciando o servidor Flask
    tmdb.run(host="0.0.0.0", port=5001, debug=True)