from fastapi import HTTPException
from http import HTTPStatus
from typing import List
from schema import CreateReceita, Receita

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

