from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_config import get_db
from schemas.aluno import Aluno, AlunoCreate
from crud import alunos as crud_alunos
from typing import List

from utils.avaliador import avaliar_tentativa
from utils.modelo_pedagogico import fornecer_feedback_aluno
from utils.resolvedor import gerar_codigo


router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.post("/", response_model=Aluno)
def create_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return crud_alunos.create_aluno(db, aluno)


@router.get("/", response_model=List[Aluno])
def read_alunos(db: Session = Depends(get_db)):
    return crud_alunos.get_alunos(db)


@router.get("/{aluno_id}", response_model=Aluno)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = crud_alunos.get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno


@router.delete("/{aluno_id}")
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = crud_alunos.delete_aluno(db, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"ok": True}

@router.post("/{aluno_id}/exercicios/{exercicio_id}/avaliar_solucao")
def avaliar_exercicio(
    aluno_id: int,
    exercicio_id: int,
    codigo: str, 
    db: Session = Depends(get_db) 
):
    """
    Endpoint para corrigir o código de um exercício submetido por um aluno.
    """
    db_aluno = crud_alunos.get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    passou, pontos_ganhos = avaliar_tentativa(db=db, exercicio_id=exercicio_id, aluno_id=aluno_id, codigo_aluno=codigo)

    feedback = fornecer_feedback_aluno(exercicio_id=exercicio_id, resposta_aluno=codigo)

    return {
        "aluno_id": aluno_id,
        "exercicio_id": exercicio_id,
        "passou_testes": passou,
        "pontos_ganhos": pontos_ganhos,
        "feedback": feedback
    }

#pedir resolucao do exercicio   
@router.post("/{aluno_id}/exercicios/{exercicio_id}/resolver")
def resolver_exercicio(aluno_id: int, exercicio_id: int, codigo: str, db: Session = Depends(get_db)):
    """Endpoint para submeter o código de um exercício por um aluno.
    """
    db_aluno = crud_alunos.get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    resolucao, resultado_execucao = gerar_codigo(exercicio_id=exercicio_id)

    return {"aluno_id": aluno_id, "exercicio_id": exercicio_id, "codigo_submetido": codigo, "resolucao": resolucao, "resultado_execucao": resultado_execucao}

#pedir dicas e feedback do aluno em relaçaõ a 1 exercicio específico
@router.post("/{aluno_id}/feedback")
def pedir_feedback(aluno_id: int, exercicio_id: int, codigo: str, db: Session = Depends(get_db)):
    """
    Endpoint para pedir feedback sobre um exercício específico.
    """
    db_aluno = crud_alunos.get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    feedback = fornecer_feedback_aluno(exercicio_id=exercicio_id, resposta_aluno=codigo)
    return {"aluno_id": aluno_id, "exercicio_id": exercicio_id, "feedback": feedback}
