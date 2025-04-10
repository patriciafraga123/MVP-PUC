"""
  Projeto: My Movies
  Aluna: Patricia Fraga
  Curso: Pós-Graduação em Engenharia de Software - PUC-Rio
  Data: Abril/2025
  Arquivo: model/__init__.py – Inicialização do banco de dados (minha_api)

  Descrição:
    Este módulo configura a conexão com o banco de dados PostgreSQL para a API principal (minha_api).
    Utiliza SQLAlchemy para definir o mecanismo de conexão (engine), criar sessões de acesso (Session)
    e garantir que o banco de dados e as tabelas necessárias existam ao iniciar o sistema.

    Funcionalidades:
      - Lê a URL do banco a partir da variável de ambiente DATABASE_URL 
      - Verifica se o banco já existe; caso contrário, cria o banco automaticamente
      - Cria todas as tabelas definidas nos arquivos de modelo 
"""

import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model.base import Base
from model.comentario import Comentario
from model.filme import Filme

db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@db_minha_api:5432/meubanco_minha_api")

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
