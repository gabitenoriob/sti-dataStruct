from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import TentativaAluno
from utils.avaliador import avaliar_tentativa


router = APIRouter(prefix="/tentativas", tags=["Tentativas"])


@router.patch("/avaliar/{tentativa_id}/{aluno_id}")
def avaliar(tentativa_id: int, aluno_id: int,  db: Session = Depends(get_db)):
    #verificar se a tentativa passa nos casos testes e se sim = concluida
    tentativa = avaliar_tentativa(db, tentativa_id)
    return {
        "tentativa_id": tentativa.id,
        "concluido": tentativa.concluido,
        "aluno_id": aluno_id
    }


@router.get("/{aluno_id}")
def listar_tentativas(aluno_id: int, db: Session = Depends(get_db)):
    tentativas = db.query(TentativaAluno).filter(TentativaAluno.aluno_id == aluno_id).all()
    return tentativas
