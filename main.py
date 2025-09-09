from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title='API do Kaué e do Gustavo')


class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(CreateReceita):
    id: int


receitas: List[Receita] = []
contador_id = 1


@app.get("/receitas")
def get_todas_receitas():
    return receitas


@app.get("/receitas/{nome_receita}")
def get_receitas_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    return {"erro": "Receita não encontrada"}


@app.post("/receitas")
def create_receita(dados: CreateReceita):
    global contador_id

    nova_receita = Receita(
        id=contador_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    contador_id += 1

    return nova_receita


@app.put("/receitas/{id}")
def update_receita(id: int, dados: CreateReceita):
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

    return {"erro": "Receita não encontrada"}


def buscar_receita(id_receita: int) -> dict:
    for receita in receitas:
        if receita.id == id_receita:
            return receita
    return {"mensagem": "Receita não encontrada"}
