# Inicializa o módulo de models, permitindo importar todos os modelos do diretório.

"""
  Projeto: Filmes Populares API
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC-Rio
  Data: Abril/2025
  Arquivo: model/__init__.py – Inicialização do banco de dados (filmespop_api)

  Descrição:
    Este módulo configura a conexão com o banco de dados PostgreSQL para a API de filmes populares (filmespop_api).
    Utiliza SQLAlchemy para definir o mecanismo de conexão (engine), criar sessões de acesso (Session)
    e garantir que o banco de dados e suas tabelas estejam criados corretamente ao iniciar o sistema.

  Funcionalidades:
    - Lê a URL do banco de dados a partir da variável de ambiente DATABASE_URL 
    - Verifica se o banco já existe; caso contrário, cria automaticamente
    - Cria todas as tabelas definidas nos modelos do diretório model/
"""

import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model.base import Base
from model.filmepop import FilmePop

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@db_filmespop_api:5432/meubanco_filmespop_api")

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)


Base.metadata.create_all(engine)

