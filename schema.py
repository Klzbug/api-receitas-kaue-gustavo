from pydantic import BaseModel
from typing import List

class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(CreateReceita):
    id: int

class Usuario(BaseModel):
    id: int
    nome: str
    email: str

