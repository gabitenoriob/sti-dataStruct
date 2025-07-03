#new file 

def calcular_pontuacao(exercicio):
    nivel = exercicio.nivel_dificuldade.lower()
    return {
        "facil": 10,
        "medio": 20,
        "dificil": 30
    }.get(nivel, 10)


def update_pontuacao(db, aluno, exercicio):
    pontos = calcular_pontuacao(exercicio)
    
    if aluno.pontuacao_total is None:
        aluno.pontuacao_total = 0

    aluno.pontuacao_total += pontos
    db.flush()
    db.commit()
