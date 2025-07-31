import streamlit as st
import pandas as pd

# Carrega o arquivo Excel
df = pd.read_excel("exported_leads.xlsx")

# Converte a coluna de data para datetime, ajuste o nome se necessário
df["chat_criado_em"] = pd.to_datetime(df["chat_criado_em"])

st.title("Dashboard de Leads")

# Filtro por intervalo de datas
data_min = df["chat_criado_em"].min()
data_max = df["chat_criado_em"].max()
data_inicio, data_fim = st.date_input("Selecione o intervalo de datas", [data_min, data_max])

df = df[(df["chat_criado_em"] >= pd.to_datetime(data_inicio)) & (df["chat_criado_em"] <= pd.to_datetime(data_fim))]

# Filtro por projeto
projetos = df["projeto"].unique()
projeto_selecionado = st.selectbox("Selecione o projeto", options=projetos)

df_filtrado = df[df["projeto"] == projeto_selecionado]

# Mostrar dados básicos
st.write("Total de leads:", len(df_filtrado))

# Mostrar quantidade por status
status_counts = df_filtrado["status"].value_counts()
st.bar_chart(status_counts)

# Mostrar tabela filtrada
st.write("Leads do projeto selecionado:")
st.dataframe(df_filtrado.drop(columns=["historico"], errors="ignore"))  # remove a coluna historico, se existir

# Histórico das conversas
st.subheader("Histórico das Conversas")

for idx, row in df_filtrado.iterrows():
    st.markdown(f"**Lead ID:** {row['lead_id']}")
    st.markdown(f"**Status:** {row['status']}")
    st.markdown(f"**Nome:** {row.get('nome', 'N/A')}")
    st.markdown(f"**Telefone:** {row.get('telefone', 'N/A')}")

    url = row.get('chat_history_url', '')
    if isinstance(url, str) and url.strip():
        st.markdown(f"[Ver conversa]({url})")
    else:
        st.markdown("_Sem link para conversa._")

    st.write("---")
