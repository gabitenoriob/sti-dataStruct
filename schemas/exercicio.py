from typing import Optional
from typing import List

from pydantic import BaseModel
class DicaSchema(BaseModel):
    
    id: int
    conteudo: str 

    class Config:
        from_attributes = True 


class CasoTesteSchema(BaseModel):
    entrada: str
    saida_esperada: str

    class Config:
        from_atributtes = True


class ExercicioBase(BaseModel):
    enunciado: str
    nivel_dificuldade: str
    solucao_esperada: str
    estrutura_id: int
    tempo_ideal: Optional[str]
    espaco_ideal: Optional[str]
    dicas: Optional[List[DicaSchema]] = None
    casos_teste: Optional[List[CasoTesteSchema]] = None

    class Config:
        from_atributtes = True




class ExercicioCreate(ExercicioBase):
    pass


class Exercicio(ExercicioBase):
    id: int

    class Config:
        from_attributes = True  