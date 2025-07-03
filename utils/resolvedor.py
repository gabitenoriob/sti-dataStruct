import os
import google.generativeai as genai
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import Exercicio, CasoTeste
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key do Google não encontrada. Verifique seu arquivo .env")

genai.configure(api_key=api_key)

def gerar_codigo(exercicio_id: int):
    db: Session = next(get_db())

    try:
        # Busca o exercício no banco
        exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if not exercicio:
            raise ValueError(f"Exercício com id {exercicio_id} não encontrado.")

        # Busca os casos de teste
        casos = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()

        casos_texto = "\n".join([f"Input: {c.entrada}\nExpected Output: {c.saida_esperada}" for c in casos])

        prompt = f"""
Você é um solucionador de problemas especialista em Python.
Escreva uma função em Python que resolva o seguinte problema:

{exercicio.enunciado}

A função deve se chamar 'solucao'.

A função deve passar nos seguintes casos de teste. Inclua a função e chamadas print() para os testes.

{casos_texto}

Escreva apenas o código Python dentro de um bloco de código markdown. Não adicione nenhuma explicação fora do bloco de código.
"""

        # Usa o modelo direto
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            prompt,
            # tools=[genai.tools.CodeExecutionTool()]
        )

        codigo_gerado = None
        output_execucao = None

        for part in response.candidates[0].content.parts:
            if part.executable_code:
                codigo_gerado = part.executable_code.code
            if part.code_execution_result:
                output_execucao = part.code_execution_result.output

        if not codigo_gerado:
            raise ValueError("Não foi possível gerar o código.")

        return {
            "codigo": codigo_gerado,
            "resultado_execucao": output_execucao
        }


    finally:
        db.close()
