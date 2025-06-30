from sqlalchemy.orm import Session
from models import Exercicio
from schemas.exercicio import ExercicioCreate


def create_exercicio(db: Session, exercicio: ExercicioCreate):
    db_exercicio = Exercicio(**exercicio.dict())
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio


def get_exercicios(db: Session):
    return db.query(Exercicio).all()


def get_exercicio(db: Session, exercicio_id: int):
    return db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()


def delete_exercicio(db: Session, exercicio_id: int):
    exercicio = get_exercicio(db, exercicio_id)
    if exercicio:
        db.delete(exercicio)
        db.commit()
    return exercicio
