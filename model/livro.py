from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base, Comentario

class Livro(Base):
   __tablename__ = 'livro' 

   id = Column("id", Integer, primary_key=True)
   nome = Column(String(140), unique=True)
   autor = Column(String(140))
   editora = Column(String(140))
   tipo_livro=Column(String(20))
   valor = Column(Float)
   data_insercao = Column(DateTime, default=datetime.now())
    # Definição do relacionamento entre o livro e o comentário.
   comentarios = relationship("Comentario")
   def __init__(self, nome:str,autor:str, editora:str,tipo_livro:str, valor:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do livro
            autor: autor que escrveu o livro.
            editora: editora do livro
            tipo_livro:
            valor: valor esperado para o produto
            data_insercao: data de quando o livro foi inserido à base
        """
        self.nome = nome
        self.autor=autor
        self.editora = editora
        self.tipo_livro=tipo_livro
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
   def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Livro
        """
        self.comentarios.append(comentario)        