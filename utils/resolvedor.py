#retorna a solução de um exercício
from http.client import HTTPException
from db_config import get_db
from models import Exercicio, TentativaAluno

def resolver_exercicio(exercicio_id):
    #acessa o banco de dados para pegar a solução do exercício
    with get_db().begin() as session:
        exercicio = session.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if not exercicio or not exercicio.solucao_esperada:
            raise HTTPException(status_code=404, detail="Solução não encontrada.")
        return exercicio.solucao_esperada