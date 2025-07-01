#retorna a solução de um exercício
import os
from google import genai
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import Exercicio, CasoTeste
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key do Google não encontrada. Verifique seu arquivo .env")
genai.configure(api_key=api_key)


def gerar_codigo(exercicio_id: int):
    db: Session = next(get_db())
    
    try: 
        exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if not exercicio:
            raise ValueError(f"Exercício com id {exercicio_id} não encontrado.")

        casos = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()

        casos_texto = ""
        for c in casos:
            casos_texto += f"\nInput: {c.entrada}\nExpected Output: {c.saida_esperada}\n"

        prompt = f"""
Você é um solucionador de problemas de programação especialista em Python.
Escreva uma função em Python que resolva o seguinte problema:

{exercicio.enunciado}

A função deve se chamar 'solucao'.

A função deve passar nos seguintes casos de teste. Forneça o código completo, incluindo a função e a execução dos testes para verificação.
Use a função print() para mostrar a saída de cada teste.

{casos_texto}

Escreva apenas o código Python dentro de um único bloco de código markdown. Não adicione nenhuma explicação fora do bloco de código.
"""

        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(prompt)

        
        
        print("--- Resposta Bruta do Gemini ---")
        print(response.text)
        print("--------------------------------\n")
        
        codigo_gerado = response.text
        if codigo_gerado.strip().startswith("```python"):
            codigo_gerado = codigo_gerado.strip()[9:-3].strip()
        elif codigo_gerado.strip().startswith("```"):
             codigo_gerado = codigo_gerado.strip()[3:-3].strip()


        print("--- Código Extraído para Execução ---")
        print(codigo_gerado)
        print("-------------------------------------\n")

        print("--- Resultado da Execução do Código Gerado ---")
       
        try:
            exec(codigo_gerado)
        except Exception as e:
            print(f"\nOcorreu um erro ao executar o código gerado: {e}")
        print("----------------------------------------------")


    finally:
        db.close() 
        return codigo_gerado

