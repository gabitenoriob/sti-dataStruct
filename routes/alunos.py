from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_config import get_db
from schemas.aluno import Aluno, AlunoCreate
from crud import alunos as crud_alunos
from typing import List


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
