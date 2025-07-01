
import datetime
from models import Exercicio, TentativaAluno
from db.db_config import get_db
from typing import Tuple 
from sqlalchemy.orm import Session

import sys
import io
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import TentativaAluno, CasoTeste


def executar_codigo(codigo: str, entrada: dict):
    """
    Executa o código enviado, chamando uma função esperada.
    :param codigo: Código enviado (string contendo uma classe Solution com função target).
    :param entrada: Dicionário com os inputs.
    :return: Saída da função.
    """

    # Ambiente isolado
    ambiente = {}

    try:
        exec(codigo, ambiente)  # Executa a classe Solution no ambiente isolado
        solution = ambiente["Solution"]()  # Instancia a classe Solution

        # Identificar qual função tem na classe Solution
        func = next(
            (getattr(solution, attr) for attr in dir(solution) if not attr.startswith("__")),
            None
        )

        if not func:
            raise Exception("Nenhuma função encontrada na classe Solution.")

        resultado = func(**entrada)  # Chama a função passando os parâmetros
        return resultado

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao executar o código: {e}")

import json
def parse_entrada(entrada_str: str):
    """
    Converte a string do campo entrada do caso de teste em um dicionário.
    Exemplo de entrada_str: 'nums = [1,2,3,3]'
    Retorna: {'nums': [1,2,3,3]}
    """
    try:
        var, value = entrada_str.split("=")
        var = var.strip()
        value = value.strip()
        return {var: eval(value)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar a entrada: {e}")


def avaliar_tentativa(db: Session, exercicio_id: int, aluno_id: int, codigo_aluno: str) -> Tuple[bool, int]:
    """
    Avalia o código submetido por um aluno para um exercício específico.

    Args:
        db: A sessão do banco de dados.
        exercicio_id: O ID do exercício a ser avaliado.
        aluno_id: O ID do aluno que submeteu o código.
        codigo_aluno: O código Python submetido pelo aluno.

    Returns:
        Uma tupla contendo:
        - um booleano (True se o código passar em todos os testes, False caso contrário)
        - um inteiro (os pontos ganhos: 10 se passar de primeira, 0 caso contrário)
    """
    exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado.")

    casos_teste = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()
    if not casos_teste:
        raise HTTPException(status_code=404, detail="Nenhum caso de teste encontrado para este exercício.")

    try:
        passou_todos = True
        for caso in casos_teste:
            entrada = parse_entrada(caso.entrada)
            output = executar_codigo(codigo_aluno, entrada)

            if str(output).strip().lower() != str(caso.saida_esperada).strip().lower():
                passou_todos = False
                break

        tentativas_anteriores = db.query(TentativaAluno).filter(
            TentativaAluno.aluno_id == aluno_id,
            TentativaAluno.exercicio_id == exercicio_id
        ).count()

        pontos = 0
        if passou_todos:
            if tentativas_anteriores == 0:
                pontos = 10
            else:
                pontos = 0

        nova_tentativa = TentativaAluno(
            aluno_id=aluno_id,
            exercicio_id=exercicio_id,
            codigo_enviado=codigo_aluno,
            concluido=passou_todos
        )
        db.add(nova_tentativa)
        db.commit()
        db.refresh(nova_tentativa)

        return passou_todos, pontos

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro durante a execução ou avaliação do código: {e}")



def pode_fazer_exercicio(db: Session, aluno_id: int, exercicio: Exercicio) -> bool:
    dependencias = exercicio.dependencias_origem
    if not dependencias:
        return True  

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
