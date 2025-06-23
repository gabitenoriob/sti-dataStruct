router = APIRouter()
from fastapi import HTTPException
from models.teste import CasoTesteCreate
from db import get_connection

@router.post("/testes/")
def criar_caso_teste(caso: CasoTesteCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO caso_teste (entrada, saida_esperada, exercicio_id) VALUES (%s, %s, %s)",
            (caso.entrada, caso.saida_esperada, caso.exercicio_id)
        )
        conn.commit()
        return {"status": "Caso de teste criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()