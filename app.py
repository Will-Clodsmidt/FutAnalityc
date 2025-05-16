import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Sistema de Previsão de Partidas de Futebol")
st.subheader("Campeonato Brasileiro - Séries A, B e C")

# Carregar dados com previsões (exemplo com Série A e Poisson)
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Arquivo de dados não encontrado: {file_path}. Verifique se o arquivo está no mesmo diretório que o app.py no repositório GitHub e se o nome está correto.")
        return pd.DataFrame()

# O caminho do arquivo de dados deve ser relativo ao local do app.py no repositório
data_path = "serie_a_com_previsoes_poisson.csv"
df_predictions = load_data(data_path)

if not df_predictions.empty:
    st.header("Previsões de Gols (Modelo Poisson) - Série A")
    
    # Placeholders para filtros
    st.sidebar.header("Filtros")
    st.info("Filtros para times, datas e campeonatos serão adicionados aqui.")

    # Exibir uma amostra das previsões
    st.dataframe(df_predictions)
    
    # Estatísticas básicas
    st.subheader("Estatísticas das Previsões")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Média de Gols Previstos (Mandante)", f"{df_predictions['pred_gols_mandante'].mean():.2f}")
        st.metric("Máximo de Gols Previstos (Mandante)", f"{df_predictions['pred_gols_mandante'].max():.2f}")
    
    with col2:
        st.metric("Média de Gols Previstos (Visitante)", f"{df_predictions['pred_gols_visitante'].mean():.2f}")
        st.metric("Máximo de Gols Previstos (Visitante)", f"{df_predictions['pred_gols_visitante'].max():.2f}")
    
    st.markdown("--- ")
    st.markdown("**Observações:**")
    st.markdown("- Este é um painel em desenvolvimento.")
    st.markdown("- As previsões atuais são baseadas no modelo de Poisson para a Série A.")
    st.markdown("- Funcionalidades adicionais, incluindo o modelo XGBoost, dados das Séries B e C, e mais filtros, serão implementadas.")
else:
    st.warning("Não foi possível carregar os dados de previsão. Verifique se o arquivo 'serie_a_com_previsoes_poisson.csv' está presente no repositório GitHub junto com o app.py e se as etapas anteriores de coleta e modelagem foram executadas corretamente para gerar este arquivo.")
