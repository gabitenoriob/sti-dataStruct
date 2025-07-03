import re
import subprocess
import tempfile
import textwrap
from typing import Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Exercicio, CasoTeste, TentativaAluno

def detectar_metodo(codigo: str) -> str:
    """Detecta o nome do primeiro método da classe Solution no código do aluno."""
    match = re.search(r"def\s+(\w+)\s*\(", codigo)
    if match:
        return match.group(1)
    raise ValueError("Nenhum método encontrado no código.")

def executar_codigo(codigo_aluno: str, entrada: any) -> str:
    """Executa o código do aluno com a entrada fornecida usando subprocess e retorna a saída."""
    try:
        metodo = detectar_metodo(codigo_aluno)

        if isinstance(entrada, (list, tuple)):
            entrada_formatada = repr(tuple(entrada))
        else:
            entrada_formatada = f"({repr(entrada)},)"

        codigo_execucao = f"""

{codigo_aluno}

if __name__ == "__main__":
    sol = Solution()
    resultado = sol.{metodo}{entrada_formatada}
    print(resultado)
"""

        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as temp_file:
            temp_file.write(textwrap.dedent(codigo_execucao))
            temp_file.flush()

            result = subprocess.run(
                ["python", temp_file.name],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip())

            return result.stdout.strip()

    except subprocess.TimeoutExpired:
        raise RuntimeError("Execução excedeu o tempo limite.")
    except Exception as e:
        raise RuntimeError(f"Erro durante execução: {e}")

def parse_entrada(entrada_str: str):
    """Converte a string de entrada salva no banco em uma estrutura Python válida."""
    try:
        return eval(entrada_str, {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Erro ao interpretar a entrada: {e}")

def avaliar_tentativa(db: Session, exercicio_id: int, aluno_id: int, codigo_aluno: str) -> Tuple[bool, int]:
    """Avalia se o código do aluno passa em todos os testes. Retorna se passou e os pontos."""
    print(f"Código do aluno recebido:\n{codigo_aluno}")

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
            saida_obtida = executar_codigo(codigo_aluno, entrada)

            if str(saida_obtida).strip().lower() != str(caso.saida_esperada).strip().lower():
                passou_todos = False
                break

        tentativas_anteriores = db.query(TentativaAluno).filter(
            TentativaAluno.aluno_id == aluno_id,
            TentativaAluno.exercicio_id == exercicio_id
        ).count()

        pontos = 10 if passou_todos and tentativas_anteriores == 0 else 0

        nova_tentativa = TentativaAluno(
            aluno_id=aluno_id,
            exercicio_id=exercicio_id,
            codigo_enviado=codigo_aluno,
            concluido=passou_todos
        )
        db.add(nova_tentativa)
        db.commit()

        return passou_todos, pontos

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na execução ou avaliação do código: {e}")


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
