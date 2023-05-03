from pydantic import BaseModel
from typing import Optional, List
from model.livro import Livro
from schemas import ComentarioSchema

class LivroSchema(BaseModel):
     """Define como um novo livro a ser inserido deve ser representado"""
     nome: str="O Alquimista"
     autor: str="Paulo Coelho"
     editora: str="Companhia das Letras"
     tipo_livro: str="Fisico"
     valor: float= 50.0

class LivroBuscaSchema(BaseModel):
     """
Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do livro.
     """
     nome:str="O Alquimista"
class ListagemLivrosSchema(BaseModel):
     """ Define como uma listagem de livros será retornada."""
     livros: List[LivroSchema]
def apresenta_livros(livros: List[Livro]):
     """
     Retorna uma representação do livro seguindo o schema definido em
      LivroViewSchema.
     """
     result = []
     for livro in livros:
          result.append({
               "nome":livro.nome,
               "autor":livro.autor,
               "editora": livro.editora,
               "tipo_livro":livro.tipo_livro,
               "valor":livro.valor
          })

          return {"livros":result}
class LivroViewSchema(BaseModel):
     """Define como um livro será retornado"""
     id: int=1
     nome: str="O Alquimista"
     autor: str="Paulo Coelho"
     editora: str="Companhia das Letras"
     tipo_livro: str="Fisico"
     valor: float= 50.0
     total_cometarios: int = 1
     comentarios:List[ComentarioSchema]       
class LivroDelSchema(BaseModel):
    
    message:str
    nome:str

def apresenta_livro(livro:Livro):
     """
     Retorna uma representação do livro seguindo o schema definido em
       LivroViewSchema.
     """
     return{
          "id": livro.id,
           "nome":livro.nome,
           "autor":livro.autor,
           "editora": livro.editora,
           "tipo_livro":livro.tipo_livro,
           "valor":livro.valor,
          "total_cometarios": len(livro.comentarios),
          "comentarios": [{"texto": c.texto} for c in livro.comentarios]
     }