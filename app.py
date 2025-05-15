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
        # Converter colunas de data se necessário
        if 'data' in df.columns:
            df['data'] = pd.to_datetime(df['data'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Arquivo de dados não encontrado: {file_path}. Verifique se o modelo já foi treinado e os dados processados.")
        return pd.DataFrame()

data_path = "/home/ubuntu/serie_a_com_previsoes_poisson.csv"
df_predictions = load_data(data_path)

if not df_predictions.empty:
    st.header("Previsões de Gols (Modelo Poisson) - Série A")
    
    # Placeholders para filtros
    st.sidebar.header("Filtros")
    # Adicionar filtros reais posteriormente
    # Exemplo: times_disponiveis = sorted(pd.concat([df_predictions['time_mandante'], df_predictions['time_visitante']]).unique())
    # time_selecionado = st.sidebar.multiselect("Selecione os Times", times_disponiveis)
    # data_inicio = st.sidebar.date_input("Data Início")
    # data_fim = st.sidebar.date_input("Data Fim")

    st.info("Filtros para times, datas e campeonatos serão adicionados aqui.")

    # Exibir uma amostra das previsões
    st.dataframe(df_predictions[['data', 'time_mandante', 'time_visitante', 'gols_mandante', 'gols_visitante', 'pred_gols_mandante', 'pred_gols_visitante']].head(20))
    
    st.markdown("--- ")
    st.markdown("**Observações:**")
    st.markdown("- Este é um painel em desenvolvimento.")
    st.markdown("- As previsões atuais são baseadas no modelo de Poisson para a Série A.")
    st.markdown("- Funcionalidades adicionais, incluindo o modelo XGBoost, dados das Séries B e C, e mais filtros, serão implementadas.")
else:
    st.warning("Não foi possível carregar os dados de previsão. Execute as etapas anteriores de coleta e modelagem.")

# Para executar este painel: streamlit run nome_do_arquivo.py

