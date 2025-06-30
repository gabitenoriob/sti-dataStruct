from typing import Optional

from pydantic import BaseModel


class TentativaBase(BaseModel):
    codigo_enviado: str
    resultado: Optional[str]
    tempo_gasto: Optional[int]
    aluno_id: int
    exercicio_id: int


class TentativaCreate(TentativaBase):
    pass


class Tentativa(TentativaBase):
    id: int
    class Config:
        orm_mode = True