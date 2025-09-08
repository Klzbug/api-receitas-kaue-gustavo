from pydantic import BaseModel
from typing import List



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


@app.get("/receitas")
def listar_receitas():
    return receitas


@app.get("/receitas/{nome}")
def buscar_receita(nome: str):
    for receita in receitas:
        if receita.nome == nome.lower():
            return receita
    return {"erro": "Receita não encontrada"}


@app.post("/receitas")
def create_receita(dados: Receita):
    nova_receita = dados

    receitas.append(nova_receita)

    return nova_receita

