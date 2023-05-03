from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from model import Session, Livro, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
livro_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um livro cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/livro',tags=[livro_tag],
          responses={"200": LivroViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_livro(form: LivroSchema):
    
    livro= Livro(
        nome=form.nome,
        autor=form.autor,
        editora=form.editora,
        tipo_livro=form.tipo_livro,
        valor=form.valor)
    logger.debug(f"Adicionando livro de nome: '{livro.nome}'")
    logger.debug(form)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(livro)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{livro.nome}'")
        return apresenta_livro(livro), 200
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar livro '{livro.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar livro '{livro.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/livros',tags=[livro_tag],
        responses={"200": ListagemLivrosSchema, "404": ErrorSchema})
def get_livros():
    """
    Faz a busca por todos os Livros cadastrados

    Retorna uma representação da listagem de livros.
    """
    logger.debug(f"Coletando livros ")
    # criando conexão com a base
    session = Session()
    # fazendo busca
    livros = session.query(Livro).all()
    print(livros)
    if not livros:
        # se não há livros cadastrados
        return {"livros": []}, 200
    else:
        logger.debug(f"%d livros econtrados" % len(livros))
        # retorna a representação de produto
        print(livros)
        return apresenta_livros(livros), 200
@app.get('/livro',tags=[livro_tag],
        responses={"200": LivroViewSchema, "404": ErrorSchema} ) 
def get_livro(query:LivroBuscaSchema):
    """
    Faz a busca por um Livro a partir do id do livro

    Retorna uma representação dos livros e comentários associados.
    """
    nome=query.nome
    logger.debug(f"Coletando dados sobre livro #{nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca 
    livro= session.query(Livro).filter(Livro.nome==nome).first()
    if not livro:
        # se o produto não foi encontrado
        error_msg = "Livro não encontrado na base :/"
        logger.warning(f"Erro ao buscar livro '{nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Livro encontrado: '{livro.nome}'")
        # retorna a representação de livro
        return apresenta_livro(livro), 200

@app.delete('/livro', tags=[livro_tag],
             responses={"200": LivroDelSchema, "404": ErrorSchema})
def del_livro(query:LivroBuscaSchema):
    """
    Deleta um Livro a partir do id de livro informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome= unquote(unquote(query.nome))
    print(nome)
    logger.debug(f"Deletando dados sobre livro #{nome}")
    #criando conexão com a base
    session= Session()
    #fazendo remoção
    count= session.query(Livro).filter(Livro.nome==nome).delete()
    session.commit()
    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado livro #{nome}")
        return {"mesage": "Livro removido", "id": nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar livro #'{nome}', {error_msg}")
        return {"mesage": error_msg}, 404
@app.post('/cometario', tags=[comentario_tag],
          responses={"200": LivroViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """
     Adiciona  um novo comentário à um livro cadastrado na base identificado pelo id

    Retorna uma representação dos livros e comentários associados.
    """
    id  = form.id
    logger.debug(f"Adicionando comentários ao produto #{id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    livro = session.query(Livro).filter(livro.id == id).first()

    if not livro:
        # se livro não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao produto '{id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao livro
    livro.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao produto #{id}")

    # retorna a representação de um livro
    return apresenta_livro(livro), 200

