from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def get_connection():
    load_dotenv()

    USER = os.getenv("user")
    PASSWORD = os.getenv("password").strip()
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    return USER, PASSWORD, HOST, PORT, DBNAME

USER, PASSWORD, HOST, PORT, DBNAME = get_connection()

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


engine = create_engine(DATABASE_URL)

Base = declarative_base()

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")
    
# Tabelas

class EstruturaDeDado(Base):
    __tablename__ = 'estrutura_dado'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text)
    exercicios = relationship("Exercicio", back_populates="estrutura")

class Exercicio(Base):
    __tablename__ = 'exercicio'
    id = Column(Integer, primary_key=True)
    enunciado = Column(Text, nullable=False)
    nivel_dificuldade = Column(String)
    solucao_esperada = Column(Text)
    estrutura_id = Column(Integer, ForeignKey('estrutura_dado.id'))
    estrutura = relationship("EstruturaDeDado", back_populates="exercicios")
    casos_teste = relationship("CasoTeste", back_populates="exercicio")
    tentativas = relationship("TentativaAluno", back_populates="exercicio")
    dependencias_origem = relationship(
        "DependenciaExercicio",
        back_populates="exercicio_origem",
        foreign_keys="DependenciaExercicio.exercicio_origem_id"
    )

    dependencias_destino = relationship(
        "DependenciaExercicio",
        back_populates="exercicio_destino",
        foreign_keys="DependenciaExercicio.exercicio_destino_id"
    )


class DependenciaExercicio(Base):
    __tablename__ = 'dependencia_exercicio'

    id = Column(Integer, primary_key=True)
    exercicio_origem_id = Column(Integer, ForeignKey('exercicio.id'))
    exercicio_destino_id = Column(Integer, ForeignKey('exercicio.id'))

    exercicio_origem = relationship(
        "Exercicio",
        back_populates="dependencias_origem",
        foreign_keys=[exercicio_origem_id]
    )

    exercicio_destino = relationship(
        "Exercicio",
        back_populates="dependencias_destino",
        foreign_keys=[exercicio_destino_id]
    )

    
class CasoTeste(Base):
    __tablename__ = 'caso_teste'
    id = Column(Integer, primary_key=True)
    entrada = Column(Text, nullable=False)
    saida_esperada = Column(Text, nullable=False)
    exercicio_id = Column(Integer, ForeignKey('exercicio.id'))
    exercicio = relationship("Exercicio", back_populates="casos_teste")

class Aluno(Base):
    __tablename__ = 'aluno'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    nivel_conhecimento = Column(String)
    historico = relationship("HistoricoDesempenho", back_populates="aluno")
    tentativas = relationship("TentativaAluno", back_populates="aluno")

class HistoricoDesempenho(Base):
    __tablename__ = 'historico_desempenho'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    aluno_id = Column(Integer, ForeignKey('aluno.id'))
    aluno = relationship("Aluno", back_populates="historico")

class TentativaAluno(Base):
    __tablename__ = 'tentativa_aluno'
    id = Column(Integer, primary_key=True)
    codigo_enviado = Column(Text)
    resultado = Column(String)
    tempo_gasto = Column(Integer)
    aluno_id = Column(Integer, ForeignKey('aluno.id'))
    exercicio_id = Column(Integer, ForeignKey('exercicio.id'))
    aluno = relationship("Aluno", back_populates="tentativas")
    exercicio = relationship("Exercicio", back_populates="tentativas")
    codigos = relationship("CodigoSubmetido", back_populates="tentativa")

class CodigoSubmetido(Base):
    __tablename__ = 'codigo_submetido'
    id = Column(Integer, primary_key=True)
    conteudo = Column(Text, nullable=False)
    tentativa_id = Column(Integer, ForeignKey('tentativa_aluno.id'))
    tentativa = relationship("TentativaAluno", back_populates="codigos")

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    texto = Column(Text)
    tipo_erro = Column(String)
    sugestao_melhoria = Column(Text)

class ErroComum(Base):
    __tablename__ = 'erro_comum'
    id = Column(Integer, primary_key=True)
    descricao = Column(Text)
    tipo = Column(String)

class Operacao(Base):
    __tablename__ = 'operacao'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    complexidade_esperada = Column(String)

class Complexidade(Base):
    __tablename__ = 'complexidade'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)  
    valor_esperado = Column(String)

Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso!")
