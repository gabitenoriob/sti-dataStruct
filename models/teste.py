from pydantic import BaseModel

class CasoTesteCreate(BaseModel):
    entrada: str
    saida_esperada: str
    exercicio_id: int
