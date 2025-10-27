from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from typing import List
from schema import Receita, CreateReceita, Usuario

# --- Funções de Serviço (Migradas de services.py) ---

def validar_regras_negocio_receita(dados: CreateReceita, receitas: List[Receita], id_atual: int = None):
    """
    Valida as regras de negócio para uma receita (criação ou atualização).
    """
    # Validação de comprimento do nome
    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="O nome da receita deve ter entre 2 e 50 caracteres."
        )

    # Validação de quantidade de ingredientes
    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A receita deve ter no mínimo 1 e no máximo 20 ingredientes."
        )

    # Validação de nome duplicado (conflito)
    for receita_existente in receitas:
        # Verifica se é uma receita diferente (para PUT) ou se é uma nova receita (para POST)
        if receita_existente.nome.lower() == dados.nome.lower() and receita_existente.id != id_atual:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe uma receita com este nome."
            )

def buscar_receita_por_id(id: int, receitas: List[Receita]) -> Receita:
    """
    Busca uma receita pelo ID e levanta 404 se não for encontrada.
    """
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Receita com o ID especificado não foi encontrada"
    )

def buscar_receita_por_nome(nome_receita: str, receitas: List[Receita]) -> Receita:
    """
    Busca uma receita pelo nome e levanta 404 se não for encontrada.
    """
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail="Receita não encontrada"
    )

# --- Configuração da Aplicação ---

app = FastAPI(title='API do Kaué e do Gustavo')

receitas: List[Receita] = []
contador_id = 1

# Dados de exemplo
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

# --- Rotas da API ---

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
    # A função buscar_receita_por_id já levanta HTTPException(404) se não encontrar
    return buscar_receita_por_id(id, receitas)

@app.get("/receitas/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receitas_por_nome(nome_receita: str):
    # A função buscar_receita_por_nome já levanta HTTPException(404) se não encontrar
    return buscar_receita_por_nome(nome_receita, receitas)

@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    # Validação das regras de negócio, passando o ID atual para ignorar a receita sendo atualizada
    validar_regras_negocio_receita(dados, receitas, id_atual=id)

    # Garante que a receita existe, senão levanta 404
    # Usamos a busca para garantir o 404
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
    
    # Este código é teoricamente inalcançável, mas mantido para segurança
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada (Erro interno inesperado)")

@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    # Garante que a receita existe, senão levanta 404
    # Usamos a busca para garantir o 404
    buscar_receita_por_id(id, receitas) 

    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_removida = receitas.pop(i)
            return receita_removida
    
    # Este código é teoricamente inalcançável, mas mantido para segurança
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada (Erro interno inesperado)")
