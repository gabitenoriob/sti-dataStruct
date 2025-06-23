from fastapi import FastAPI
from routes import alunos

app = FastAPI()

# Incluindo as rotas
app.include_router(alunos.router)
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Estruturas de Dados!"}
