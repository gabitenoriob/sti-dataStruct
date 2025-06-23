from fastapi import APIRouter, HTTPException
from models.exercicio import ExercicioCreate
from db import get_connection

router = APIRouter()

@router.post("/exercicios/")
def criar_exercicio(exercicio: ExercicioCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO exercicio (enunciado, nivel_dificuldade, estrutura_id, solucao_esperada) VALUES (%s, %s, %s, %s)",
            (exercicio.enunciado, exercicio.nivel_dificuldade, exercicio.estrutura_id, exercicio.solucao_esperada)
        )
        conn.commit()
        return {"status": "Exercício criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
