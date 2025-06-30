
import datetime
from models import Exercicio, TentativaAluno
from db.db_config import get_db
from sqlalchemy.orm import Session


def avaliar_tentativa(db: Session, tentativa_id: int, sucesso: bool):
    tentativa = db.query(TentativaAluno).filter(TentativaAluno.id == tentativa_id).first()
    if not tentativa:
        raise Exception("Tentativa não encontrada.")

    if sucesso:
        tentativa.concluido = True
        tentativa.data_conclusao = datetime.now()
    else:
        tentativa.concluido = False

    db.commit()
    db.refresh(tentativa)

    return tentativa


def pode_fazer_exercicio(db: Session, aluno_id: int, exercicio: Exercicio) -> bool:
    dependencias = exercicio.dependencias_origem
    if not dependencias:
        return True  # Sem dependências, pode fazer

    for dep in dependencias:
        tentativa = (
            db.query(TentativaAluno)
            .filter(
                TentativaAluno.aluno_id == aluno_id,
                TentativaAluno.exercicio_id == dep.exercicio_destino_id,
                TentativaAluno.concluido == True,
            )
            .first()
        )
        if not tentativa:
            return False
    return True
