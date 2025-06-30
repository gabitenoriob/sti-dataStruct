from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas import exercicio
from crud import  exercicios

router = APIRouter(prefix="/exercicios", tags=["Exercícios"])


@router.post("/", response_model=exercicio.Exercicio)
def create(exercicio: exercicio.ExercicioCreate, db: Session = Depends(get_db)):
    return exercicios.create_exercicio(db, exercicio)


@router.get("/", response_model=list[exercicio.Exercicio])
def read(db: Session = Depends(get_db)):
    return exercicios.get_exercicios(db)


@router.get("/{id}", response_model=exercicio.Exercicio)
def read_one(id: int, db: Session = Depends(get_db)):
    db_item = exercicios.get_exercicio(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return db_item


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    db_item = exercicios.delete_exercicio(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return {"ok": True}
