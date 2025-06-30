from typing import Optional
from typing import List

from pydantic import BaseModel


class ExercicioBase(BaseModel):
    enunciado: str
    nivel_dificuldade: str
    solucao_esperada: str
    estrutura_id: int
    tempo_ideal: Optional[str]
    espaco_ideal: Optional[str]
    dicas: Optional[List[str]] = []
    casos_teste: Optional[List[dict]] = []  # Cada caso de teste é um dicionário com 'entrada' e 'saida_esperada'



class ExercicioCreate(ExercicioBase):
    pass


class Exercicio(ExercicioBase):
    id: int

    class Config:
        from_attributes = True  