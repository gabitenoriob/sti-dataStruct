from sqlalchemy.orm import Session
from models import Exercicio, DependenciaExercicio
from models import DependenciaEstrutura


def get_exercicio(db: Session, exercicio_id: int):
    return db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()


def get_dependencias_exercicio(db: Session, exercicio_id: int):
    return db.query(DependenciaExercicio).filter(
        DependenciaExercicio.exercicio_destino_id == exercicio_id
    ).all()


def get_dependencias_estrutura(db: Session, exercicio_id: int):
    exercicio = get_exercicio(db, exercicio_id)
    if exercicio is None:
        return []

    dependencias = db.query(DependenciaEstrutura).filter(
        DependenciaEstrutura.estrutura_origem_id == exercicio.estrutura_id
    ).all()

    return dependencias
