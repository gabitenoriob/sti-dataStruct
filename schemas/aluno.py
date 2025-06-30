from pydantic import BaseModel
from typing import Optional, List


class AlunoBase(BaseModel):
    nome: str
    nivel_conhecimento: Optional[str] = None


class AlunoCreate(AlunoBase):
    pass


class Aluno(AlunoBase):
    id: int

    class Config:
        from_attributes = True
