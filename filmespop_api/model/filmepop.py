# Define a tabela principal 'filmepo' do banco de dados 

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from model import Base

class FilmePop(Base):
    __tablename__ = 'filmepop'

    filme_pop_id = Column(Integer, primary_key = True, unique =True)
    nome_filme_pop = Column(String(140), unique=True)
    img_pop = Column(String(100))
    nota_pop = Column(Float)
    adorei_pop = Column(String(3),nullable=True)
    watchlist_pop = Column(String(3),nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, filme_pop_id:Integer, nome_filme_pop:str, img_pop:str, nota_pop:float, adorei_pop: str, watchlist_pop:str, 
                 data_insercao:Union[DateTime, None] = None):
        self.filme_pop_id = filme_pop_id
        self.nome_filme_pop = nome_filme_pop
        self.img_pop = img_pop
        self.nota_pop = nota_pop
        self.adorei_pop = adorei_pop
        self.watchlist_pop = watchlist_pop

        if data_insercao:
            self.data_insercao = data_insercao


   