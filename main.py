from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from typing import List
from schema import Receita, CreateReceita

app = FastAPI(title='API do Kaué e do Gustavo')

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
    modo_de_preparo="Misture todos os ingredientes, coloque em uma forma untada e asse por 25 minutos a 180°C."
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

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: CreateReceita):
    global contador_id

    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter entre 2 e 50 caracteres.")
    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter no mínimo 1 e no máximo 20 ingredientes.")

    for receita_existente in receitas:
        if receita_existente.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com o mesmo nome.")

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
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita com esse ID, not existe")

@app.get("/receitas/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receitas_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    if not dados.nome or not dados.nome.strip():
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Burrro, a receita n pode ser vazia.")
    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter entre 2 e 50 caracteres.")
    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter no mínimo 1 e no máximo 20 ingredientes.")

    for r in receitas:
        if r.nome.lower() == dados.nome.lower() and r.id != id:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe outra receita com este nome.")

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

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    if not receitas:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Não há receitas para deletar.")

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_removida = receitas.pop(i)
            return receita_removida
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

