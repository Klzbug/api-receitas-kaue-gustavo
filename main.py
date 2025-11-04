from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from typing import List
from schema import Receita, CreateReceita, Usuario, BaseUsuario, UsuarioPublic

app = FastAPI(title='API do Kaué e do Gustavo')

usuarios: List[Usuario] = []
contador_usuario_id = 1
receitas: List[Receita] = []
contador_id = 1

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


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario):
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
def get_todos_usuarios():
    return [UsuarioPublic(id=u.id, nome_usuario=u.nome_usuario, email=u.email) for u in usuarios]

@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int):
    usuario = buscar_usuario_por_id(id, usuarios)
    return UsuarioPublic(id=usuario.id, nome_usuario=usuario.nome_usuario, email=usuario.email)

@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str):
    usuario = buscar_usuario_por_nome(nome_usuario, usuarios)
    return UsuarioPublic(id=usuario.id, nome_usuario=usuario.nome_usuario, email=usuario.email)

@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario):
    validar_regras_negocio_usuario(dados, usuarios, id_atual=id)

    buscar_usuario_por_id(id, usuarios)

    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_atualizado = Usuario(
                id=id,
                nome_usuario=dados.nome_usuario,
                email=dados.email,
                senha=dados.senha,
            )
            usuarios[i] = usuario_atualizado
            return UsuarioPublic(id=usuario_atualizado.id, nome_usuario=usuario_atualizado.nome_usuario, email=usuario_atualizado.email)

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado (Erro interno inesperado)")

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def deletar_usuario(id: int):
    buscar_usuario_por_id(id, usuarios)

    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_removido = usuarios.pop(i)
            return UsuarioPublic(id=usuario_removido.id, nome_usuario=usuario_removido.nome_usuario, email=usuario_removido.email)

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado (Erro interno inesperado)")


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




def validar_regras_negocio_usuario(dados: BaseUsuario, usuarios: List[Usuario], id_atual: int = None):
    # Regra 1: Email único
    for usuario_existente in usuarios:
        if usuario_existente.email.lower() == dados.email.lower() and usuario_existente.id != id_atual:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um usuário com este email."
            )
    # Regra 2: Senha deve conter letras e números (Desafio Extra)
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
            return Receita
    raise HTTPException(
        
    )
    
