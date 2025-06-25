from fastapi import FastAPI
from routes import alunos, exercicios, insert_generico, testes

app = FastAPI()
app.include_router(alunos.router)
app.include_router(exercicios.router)
app.include_router(testes.router)
app.include_router(insert_generico.router)

# Incluindo as rotas
app.include_router(alunos.router)
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Estruturas de Dados!"}
