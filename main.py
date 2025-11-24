from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from http import HTTPStatus
from typing import List
from schema import Receita, CreateReceita, Usuario, BaseUsuario, UsuarioPublic
from config import settings
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_session

# ============================
# DADOS INICIAIS DA APLICAÇÃO
# ============================

app = FastAPI(title='API do Kaué e do Gustavo')

# Listas para armazenar usuários e receitas em memória
contador_usuario_id = 1
receitas: List[Receita] = []
contador_id = 1

# ============================
#      RECEITAS PADRÃO
# ============================

receitas.append(Receita(
    id=1,
    nome="Brownie",
    ingredientes=[
        "1 xícara de manteiga derretida",
        "2 xícaras de açúcar",
        "1 xícara de cacau em pó",
        "4 ovos",
        "1 xícara de farinha de trigo",
        "1 pitada de sal"
    ],
    modo_de_preparo="Misture todos os ingredientes e coloque no forno."
))

receitas.append(Receita(
    id=2,
    nome="Bolo",
    ingredientes=[
        "3 ovos",
        "2 xícaras de açúcar",
        "3 xícaras de farinha de trigo",
        "1 xícara de leite",
        "1 colher de sopa de fermento em pó"
    ],
    modo_de_preparo="Bata os ovos com o açúcar, adicione a farinha, o leite e por fim o fermento. Asse em forno médio por 35 minutos."
))

contador_id = 3

# ==============================================
#             ROTAS - USUÁRIOS
# ==============================================
# Nesta seção estão todas as rotas responsáveis
# por criar, listar, buscar, atualizar e deletar
# usuários da aplicação.
# ==============================================

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.nome_usuario == dados.nome_usuario) | (User.email == dados.email)
        )
    )

    if db_user:
        if db_user.nome_usuario == dados.nome_usuario:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail ='Email já existe',
            )
        elif db_user.email == dados.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email já existe',
            )
        
    db_user = User(
            nome_usuario=dados.nome_usuario, senha=dados.senha, email=dados.email
        )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


    global contador_usuario_id

    validar_regras_negocio_usuario(dados, usuarios)

    novo_usuario = Usuario(
        id=contador_usuario_id,
        nome_usuario=dados.nome_usuario,
        email=dados.email,
        senha=dados.senha
    )
    usuarios.append(novo_usuario)
    contador_usuario_id += 1

    return UsuarioPublic(id=novo_usuario.id, nome_usuario=novo_usuario.nome_usuario, email=novo_usuario.email)

@app.get("/usuarios", response_model=List[UsuarioPublic], status_code=HTTPStatus.OK)
def get_todos_usuarios(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return users

@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int,  session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.id == id))
    )
    if db_user:
        return db_user
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.nome_usuario == nome_usuario))
    )
    if db_user:
        return db_user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario, session: Session = Depends(get_session)):
    
    db_user = session.scalar(select(User).where(User.id == id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    try:
        db_user.nome_usuario = dados.nome_usuario
        db_user.senha = dados.senha
        db_user.email = dados.email
        session.commit()
        session.refresh(db_user)

        return db_user
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nome de usuário ou Email já existe'
        )



@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def deletar_usuario(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    session.delete(db_user)
    session.commit()

    return db_user



#            ROTAS - RECEITAS
# ==============================================
# Nesta seção estão todas as rotas responsáveis
# por criar, listar, buscar, atualizar e deletar
# receitas da aplicação.
# ==============================================

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: CreateReceita):
    global contador_id

    validar_regras_negocio_receita(dados, receitas)

    nova_receita = Receita(
        id=contador_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    contador_id += 1

    return nova_receita

@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas

@app.get("/receitas/id/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_id(id: int):
    return buscar_receita_por_id(id, receitas)

@app.get("/receitas/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receitas_por_nome(nome_receita: str):
    return buscar_receita_por_nome(nome_receita, receitas)

@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    validar_regras_negocio_receita(dados, receitas, id_atual=id)

  
    buscar_receita_por_id(id, receitas) 

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo,
            )
            receitas[i] = receita_atualizada
            return receita_atualizada
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada (Erro interno inesperado)")

@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):

    buscar_receita_por_id(id, receitas) 

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_removida = receitas.pop(i)
            return receita_removida
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada (Erro interno inesperado)")

# ==============================================
# FUNÇÕES AUXILIARES (REGRAS DE NEGÓCIO E BUSCA)
# ==============================================
# Nesta seção estão as funções responsáveis por:
# - Validar regras de negócio de usuários e receitas;
# - Buscar usuários e receitas por ID ou nome;
# - Garantir integridade e consistência dos dados.
# ==============================================

# -------------------------------
#            USUÁRIOS
# -------------------------------

def validar_regras_negocio_usuario(dados: BaseUsuario, usuarios: List[Usuario], id_atual: int = None):
    for usuario_existente in usuarios:
        if usuario_existente.email.lower() == dados.email.lower() and usuario_existente.id != id_atual:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um usuário com este email."
            )
    if not any(char.isdigit() for char in dados.senha) or not any(char.isalpha() for char in dados.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter letras e números."
        )

def buscar_usuario_por_id(id: int, usuarios: List[Usuario]) -> Usuario:
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário com o ID especificado não foi encontrado"
    )

def buscar_usuario_por_nome(nome_usuario: str, usuarios: List[Usuario]) -> Usuario:
    for usuario in usuarios:
        if usuario.nome_usuario.lower() == nome_usuario.lower():
            return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário não encontrado"
    )

# -------------------------------
#          RECEITAS
# -------------------------------

def validar_regras_negocio_receita(dados: CreateReceita, receitas: List[Receita], id_atual: int = None):
    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O nome da receita deve ter entre 2 e 50 caracteres."
        )

    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A receita deve ter no mínimo 1 e no máximo 20 ingredientes."
        )

    for receita_existente in receitas:
        if receita_existente.nome.lower() == dados.nome.lower() and receita_existente.id != id_atual:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe uma receita com este nome."
            )

def buscar_receita_por_id(id: int, receitas: List[Receita]) -> Receita:
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Receita com o ID especifico não foi encontrada"
    )

def buscar_receita_por_nome(nome_receita: str, receitas: List[Receita]) -> Receita:
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Receita com o nome especifico não foi encontrado"
    )
    
