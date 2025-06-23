import os
import psycopg2
load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password").strip()
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Conexão com Supabase (PostgreSQL)
conn = psycopg2.connect(
    host=HOST,
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    port=PORT
)

cursor = conn.cursor()

try:
    # Inserindo Categorias de Estruturas
    cursor.execute("""
        INSERT INTO categoria_estrutura (nome) VALUES
        ('Listas'),
        ('Árvores'),
        ('Grafos'),
        ('Filas'),
        ('Pilhas'),
        ('Tabelas de Hash'),
        ('Arrays');
    """)

    # Inserindo Estruturas de Dados
    cursor.execute("""
        INSERT INTO estrutura_dado (nome, descricao, categoria_id) VALUES
        ('Array', 'Estrutura linear de tamanho fixo.', 7),
        ('Linked List', 'Lista encadeada dinâmica.', 1),
        ('Stack', 'Pilha LIFO (Last In First Out).', 5),
        ('Queue', 'Fila FIFO (First In First Out).', 4),
        ('Binary Tree', 'Árvore Binária Básica.', 2),
        ('Graph', 'Estrutura de grafos direcionados ou não.', 3),
        ('Hash Table', 'Estrutura baseada em hashing para acesso rápido.', 6);
    """)

    # Inserindo Operações
    cursor.execute("""
        INSERT INTO operacao (tipo, complexidade_esperada) VALUES
        ('Inserção em Array Dinâmico', 'O(1) Amortizado'),
        ('Busca em Lista Encadeada', 'O(n)'),
        ('Push em Pilha', 'O(1)'),
        ('Enfileirar em Fila', 'O(1)'),
        ('BFS em Grafo', 'O(V + E)'),
        ('Inserção em Árvore Binária', 'O(log n)'),
        ('Busca em Hash Table', 'O(1)');
    """)

    # Inserindo Complexidades
    cursor.execute("""
        INSERT INTO complexidade (tipo, valor_esperado) VALUES
        ('Tempo', 'O(1)'),
        ('Tempo', 'O(n)'),
        ('Tempo', 'O(log n)'),
        ('Tempo', 'O(V + E)'),
        ('Espaco', 'O(n)'),
        ('Espaco', 'O(1)');
    """)

    # Inserindo Feedbacks Genéricos
    cursor.execute("""
        INSERT INTO feedback (texto, tipo_erro, sugestao_melhoria) VALUES
        ('Erro de sintaxe: verifique a indentação e os parênteses.', 'Sintaxe', 'Reveja a formatação do código.'),
        ('Erro de lógica: a saída não corresponde ao esperado.', 'Logica', 'Revise a lógica do algoritmo.'),
        ('Problema de performance: complexidade maior que a necessária.', 'Performance', 'Tente otimizar a solução.');
    """)

    # Inserindo Erros Comuns
    cursor.execute("""
        INSERT INTO erro_comum (descricao, tipo) VALUES
        ('Loop infinito por condição mal definida.', 'Logica'),
        ('Tentativa de acessar índice fora dos limites de um array.', 'Logica'),
        ('Falta de tratamento para listas vazias.', 'Logica'),
        ('Uso incorreto de ponteiros em listas encadeadas.', 'Sintaxe');
    """)

    conn.commit()
    print("Carga base inicial inserida com sucesso!")

except Exception as e:
    print(f"Erro ao executar a carga base: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
