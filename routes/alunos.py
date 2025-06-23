from fastapi import APIRouter, HTTPException
from models.aluno import AlunoCreate
from db import get_connection

router = APIRouter()

@router.post("/alunos/")
def criar_aluno(aluno: AlunoCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO aluno (nome, nivel_conhecimento) VALUES (%s, %s)",
            (aluno.nome, aluno.nivel_conhecimento)
        )
        conn.commit()
        return {"status": "Aluno criado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
