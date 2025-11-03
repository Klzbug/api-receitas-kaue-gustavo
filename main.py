from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from typing import List
from schema import Receita, CreateReceita, Usuario, BaseUsuario, UsuarioPublic

app = FastAPI(title='API do Kaué e do Gustavo')

# ==============================
#   Dados em memória
# ==============================
usuarios: List[Usuario] = []
receitas: List[Receita] = []
contador_usuario_id = 1
contador_receita_id = 1

# ==============================
#   USUÁRIOS
# ==============================

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario):
    global contador_usuario_id

    validar_regras_negocio_usuario(dados, usuarios)

    # Verificar duplicidade de nome
    for usuario_existente in usuarios:
        if usuario_existente.nome.lower() == dados.nome.lower():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um usuário com este nome."
            )

    novo_usuario = Usuario(
        id=contador_usuario_id,
        nome=dados.nome,
        senha=dados.senha
    )
    usuarios.append(novo_usuario)
    contador_usuario_id += 1

    return UsuarioPublic(id=novo_usuario.id, nome=novo_usuario.nome)


@app.get("/usuarios", response_model=List[UsuarioPublic], status_code=HTTPStatus.OK)
def get_todos_usuarios():
    return [UsuarioPublic(id=u.id, nome=u.nome) for u in usuarios]


@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int):
    usuario = buscar_usuario_por_id(id, usuarios)
    return UsuarioPublic(id=usuario.id, nome=usuario.nome)


@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str):
    usuario = buscar_usuario_por_nome(nome_usuario, usuarios)
    return UsuarioPublic(id=usuario.id, nome=usuario.nome)


@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario):
    global usuarios

    validar_regras_negocio_usuario(dados, usuarios, id_atual=id)
    usuario = buscar_usuario_por_id(id, usuarios)

    usuario.nome = dados.nome
    usuario.senha = dados.senha

    return UsuarioPublic(id=usuario.id, nome=usuario.nome)


@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def deletar_usuario(id: int):
    global usuarios

    for i, usuario in enumerate(usuarios):
        if usuario.id == id:
            removido = usuarios.pop(i)
            return UsuarioPublic(id=removido.id, nome=removido.nome)

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")


# ==============================
#   RECEITAS
# ==============================

# Receitas de exemplo
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
contador_receita_id = 3


@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: CreateReceita):
    global contador_receita_id

    validar_regras_negocio_receita(dados, receitas)

    nova_receita = Receita(
        id=contador_receita_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    contador_receita_id += 1

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

    receita = buscar_receita_por_id(id, receitas)
    receita.nome = dados.nome
    receita.ingredientes = dados.ingredientes
    receita.modo_de_preparo = dados.modo_de_preparo
    return receita


@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    global receitas

    for i, receita in enumerate(receitas):
        if receita.id == id:
            return receitas.pop(i)

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


# ==============================
#   Funções auxiliares
# ==============================

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
        detail="Receita com o ID especificado não foi encontrada"
    )


def buscar_receita_por_nome(nome_receita: str, receitas: List[Receita]) -> Receita:
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Receita não encontrada"
    )


def validar_regras_negocio_usuario(dados: BaseUsuario, usuarios: List[Usuario], id_atual: int = None):
    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O nome do usuário deve ter entre 2 e 50 caracteres."
        )

    for usuario_existente in usuarios:
        if usuario_existente.nome.lower() == dados.nome.lower() and usuario_existente.id != id_atual:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um usuário com este nome."
            )


def buscar_usuario_por_id(id: int, usuarios: List[Usuario]) -> Usuario:
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário com o ID especificado não foi encontrado"
    )


def buscar_usuario_por_nome(nome: str, usuarios: List[Usuario]) -> Usuario:
    for usuario in usuarios:
        if usuario.nome.lower() == nome.lower():
            return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Usuário não encontrado"
    )