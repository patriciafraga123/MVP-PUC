from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Filme(Base):
    __tablename__ = 'filme'

    id = Column("pk_filme", Integer, primary_key=True)
    nome_filme = Column(String(140), unique=True)
    genero = Column(String(40))
    nota_imdb = Column(Float)
    ja_assisti = Column(String(3))
    #minha_nota = Column(Integer)
    minha_nota = Column(Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o filme e o comentário.
    # Essa relação é implicita, não está salva na tabela 'filme',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome_filme:str, genero:str, nota_imdb:float, ja_assisti:str, minha_nota:Integer, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Filme

        Arguments:
            nome_filme: nome do filme.
            genero: genero do filme
            nota_imdb: nota do filme de acordo com o site IMDB
            ja_assisti : 'Sim' ou 'Não'
            minha_nota : Nota inteira de 1 a 10
            data_insercao: data de quando o filme foi inserido à base
        """
        self.nome_filme = nome_filme
        self.genero = genero 
        self.nota_imdb = nota_imdb
        self.ja_assisti = ja_assisti
        self.minha_nota = minha_nota

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Filme
        """
        self.comentarios.append(comentario)