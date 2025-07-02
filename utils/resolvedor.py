# retorna a solução de um exercício
import os
import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse # Import for type hinting, optional but good practice
from sqlalchemy.orm import Session
from db.db_config import get_db
from models import Exercicio, CasoTeste
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key do Google não encontrada. Verifique seu arquivo .env")

# A configuração da API key com genai.configure() ainda é válida para o cliente.
genai.configure(api_key=api_key)

def gerar_codigo(exercicio_id: int):
    # Obtém uma sessão de banco de dados.
    db: Session = next(get_db())

    try:
        # Buscar o exercício
        exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()
        if not exercicio:
            raise ValueError(f"Exercício com id {exercicio_id} não encontrado.")

        # Buscar os casos de teste associados ao exercício
        casos = db.query(CasoTeste).filter(CasoTeste.exercicio_id == exercicio_id).all()

        # Montar os casos de teste em um formato de texto claro para o prompt
        casos_texto = ""
        for c in casos:
            casos_texto += f"\nInput: {c.entrada}\nExpected Output: {c.saida_esperada}\n"

        # Prompt detalhado para o modelo
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

        # --- A GRANDE MUDANÇA ESTÁ AQUI ---
        # 1. Crie uma instância do cliente principal
        client = genai.Client()

        # 2. Use o cliente para acessar os modelos e gerar conteúdo
        # O modelo 'gemini-1.5-flash' é especificado diretamente no generate_content.
        # 'contents' ainda espera uma lista.
        response: GenerateContentResponse = client.models.generate_content(
            model="gemini-1.5-flash",  # Especifique o modelo aqui
            contents=[prompt],
            # Adicione configurações de geração se necessário, por exemplo:
            # config=genai.types.GenerateContentConfig(temperature=0.1)
        )

        # Retorna o texto gerado pela resposta.
        return response.text

    finally:
        # Garante que a sessão do banco de dados seja fechada.
        db.close()