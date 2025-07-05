<<<<<<< HEAD
# STI - Estrutura de Dados com Avaliação Inteligente

Este projeto é uma plataforma de exercícios de estrutura de dados com feedback automatizado e gamificação da aprendizagem.

---

## Funcionalidades

- Cadastro de alunos e controle de pontuação
- Inserção e avaliação automática de exercícios com casos de teste
- Geração de feedbacks personalizados com IA (Gemini API)
-  Sistema de dicas por exercício
-  Histórico de tentativas e progresso
- Interface simples com Streamlit

---

## Tecnologias utilizadas

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **IA**: Google Gemini (via `google.generativeai`)
- **Frontend**: Streamlit
- **Banco de dados**: PostgreSQL (via Docker ou local)
- **Outros**: dotenv, requests, pydantic

---

## Como executar o projeto localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/sti-dataStruct.git
cd sti-dataStruct
```

2. Crie um ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o `.env` com sua chave da Gemini API:

```
GOOGLE_API_KEY=coloque_sua_chave_aqui
```

5. Inicie o backend (FastAPI):

```bash
uvicorn main:app --reload
```

6. Inicie o frontend (Streamlit):

```bash
streamlit run app.py
```

---

##  Exemplos de uso

- Acesse o Swagger UI para testar a API:
  [http://localhost:8000/docs](http://localhost:8000/docs)

- Use o app do aluno via navegador:
   [http://localhost:8501](http://localhost:8501)

---

##  Estrutura do projeto

```
sti-dataStruct/
├── app.py                  # Interface Streamlit
├── main.py                 # Inicialização do FastAPI
├── models/                 # Modelos do banco
├── routers/                # Rotas da API
├── utils/                  # Lógica de avaliação, feedback e pontuação
├── db/                     # Configuração do banco de dados
├── requirements.txt        # Dependências
└── .env                    # Variáveis de ambiente (ex: GOOGLE_API_KEY)
```

---

##  Equipe

- Gabriela Batista
- Laís Souza
- José Victor Dias

---

## Observações

- Requer conexão com a API do Gemini para gerar feedbacks com IA.
- Caso deseje testar sem IA, você pode mockar a função `fornecer_feedback_aluno` em `modelo_pedagogico.py`.

---

## Exemplos de exercícios

- Contains Duplicate
- Is Anagram
- Two Sum
- Top K Frequent Elements
- Reverse Linked List
=======
>>>>>>> 17a05b88fcb07c42db3906088848ed3e3033852