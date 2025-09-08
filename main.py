
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title='API do Kaué e do Gustavo')

class Receita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

'''
receitas = [
    {
        'nome': 'Brownie',
        'ingredientes': [
            '3 ovos',
            '6 colheres de açúcar',
            '1/2 xícara (chá) de chocolate em pó',
            '100g de manteiga',
            '1 xícara (chá) de farinha de trigo'
        ],
        'utensílios': [
            'Tigela',
            'Forma',
            'Colher de pau',
            'Forno'
        ],
        'modo_de_preparo': 'Misture todos os ingredientes em uma tigela, coloque a massa em uma forma untada e leve ao forno pré-aquecido a 180°C por cerca de 30 minutos.'
    },
]
'''

receitas: List[Receita] = []

@app.get("/receitas")
def get_todas_receitas():
    return receitas


@app.get("/receitas/{nome_receita}")
def get_receitas_por_nome(nome_receita: str):
    for receita in receitas:
        if receita.nome == nome_receita():
            return receita
    return {"erro": "Receita não encontrada"}


@app.post("/receitas")
def create_receita(dados: Receita):
    nova_receita = dados

    receitas.append(nova_receita)

    return nova_receita

@app.put("/receitas{id}")
def update_receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receitas_atualizada = Receita (
                id=id,
                nome=dados.nome,
                igredientes=dados.igredientes,
                modo_de_preparo=dados.modo_de_preparo,
            )

        receitas[i] = (receita_atualizada)
        return receita_atualizada