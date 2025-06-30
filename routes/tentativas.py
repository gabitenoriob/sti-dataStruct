from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import TentativaAluno
from utils.avaliador import avaliar_tentativa


router = APIRouter(prefix="/tentativas", tags=["Tentativas"])


@router.patch("/avaliar/{tentativa_id}")
def avaliar(tentativa_id: int, sucesso: bool, db: Session = Depends(get_db)):
    tentativa = avaliar_tentativa(db, tentativa_id, sucesso)
    return {
        "tentativa_id": tentativa.id,
        "concluido": tentativa.concluido,
        "data_conclusao": tentativa.data_conclusao
    }


@router.get("/{aluno_id}")
def listar_tentativas(aluno_id: int, db: Session = Depends(get_db)):
    tentativas = db.query(TentativaAluno).filter(TentativaAluno.aluno_id == aluno_id).all()
    return tentativas
