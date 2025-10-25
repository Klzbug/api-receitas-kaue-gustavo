from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from typing import List
from schema import Receita, CreateReceita
from .services import validar_regras_negocio_receita, buscar_receita_por_id, buscar_receita_por_nome

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

    # Validação das regras de negócio
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
    # Validação das regras de negócio, passando o ID atual para ignorar a receita sendo atualizada
    validar_regras_negocio_receita(dados, receitas, id_atual=id)

    # Garante que a receita existe, senão levanta 404
    receita_existente = buscar_receita_por_id(id, receitas) 

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

    # Este código é teoricamente inalcançável devido ao buscar_receita_por_id, mas mantido como fallback
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    # Garante que a receita existe, senão levanta 404
    receita_a_deletar = buscar_receita_por_id(id, receitas) 

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_removida = receitas.pop(i)
            return receita_removida
    
    # Este código é teoricamente inalcançável devido ao buscar_receita_por_id, mas mantido como fallback
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

