import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Portal do Aluno")

st.sidebar.header("Ações")

# Exibir pontuação
aluno_id = st.sidebar.number_input("ID do Aluno", min_value=1, step=1)

if st.sidebar.button("Ver Pontuação Total"):
    res = requests.get(f"{BASE_URL}/alunos/{aluno_id}/pontuacao_total")
    if res.status_code == 200:
        dados = res.json()
        st.success(f"Pontuação total: {dados['pontuacao_total']} pontos")
    else:
        st.error("Aluno não encontrado")

# Submeter código para avaliação
st.subheader("Submeter Código")
exercicio_id = st.number_input("ID do Exercício", min_value=1, step=1)
codigo = st.text_area("Cole seu código aqui:", height=200)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Avaliar Código"):
        payload = {"aluno_id": aluno_id, "exercicio_id": exercicio_id, "codigo": codigo}
        res = requests.post(f"{BASE_URL}/tentativas/avaliar", json=payload)
        if res.status_code == 200:
            r = res.json()
            st.success(f"Passou nos testes? {'Sim' if r['passou_testes'] else 'Não'}")
            st.info(f"Pontos ganhos: {r['pontos_ganhos']}")
        else:
            st.error("Erro ao avaliar o código.")

with col2:
    if st.button("Obter Feedback da IA"):
        params = {
            "exercicio_id": exercicio_id,
            "codigo": codigo
        }
        res = requests.post(f"{BASE_URL}/alunos/{aluno_id}/feedback", params=params)
        if res.status_code == 200:
            r = res.json()
            st.markdown("### 💡 Feedback:")
            st.info(r["feedback"])
        else:
            st.error("Erro ao obter feedback.")
            st.text(f"Status: {res.status_code}")
            st.text(f"Resposta: {res.text}")
    if st.button("Desistir e Ver Resposta"):
        params = {
            "codigo": codigo
        }
        res = requests.post(
            f"{BASE_URL}/alunos/{aluno_id}/exercicios/{exercicio_id}/resolver",
            params=params
        )
        if res.status_code == 200:
            r = res.json()
            print(r)
            st.markdown("### ✅ Solução:")
            st.info(r["resolucao_llm"])
        else:
            st.error("Erro ao obter feedback.")
            st.text(f"Status: {res.status_code}")
            st.text(f"Resposta: {res.text}")

with col3:
    if st.button("Ver Dicas do Exercício"):
        params = {
            "exercicio_id": exercicio_id,
            'codigo': "enumere dicas curtas para resolver esse exercício"
        }
        res = requests.post(f"{BASE_URL}/alunos/{aluno_id}/feedback", params=params)
        if res.status_code == 200:
            dicas = res.json()
            if dicas:
                st.markdown("### 📌 Dicas:")
                st.info(dicas["feedback"])                
        else:
            st.error("Erro ao buscar dicas.")
