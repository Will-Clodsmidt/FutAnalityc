import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema de Previsão de Futebol - Brasileirão")

# Título e descrição
st.title("Sistema de Previsão de Partidas de Futebol")
st.subheader("Campeonato Brasileiro - Séries A, B e C")

# Dados de exemplo para demonstração
def create_sample_data():
    # Criar dados de exemplo para Série A
    serie_a_data = {
        'data': pd.date_range(start='2022-01-01', periods=10),
        'time_mandante': ['Time1_SerieA', 'Time2_SerieA', 'Time3_SerieA', 'Time4_SerieA', 'Time5_SerieA',
                         'Time6_SerieA', 'Time7_SerieA', 'Time8_SerieA', 'Time9_SerieA', 'Time10_SerieA'],
        'time_visitante': ['Time11_SerieA', 'Time12_SerieA', 'Time13_SerieA', 'Time14_SerieA', 'Time15_SerieA',
                          'Time16_SerieA', 'Time17_SerieA', 'Time18_SerieA', 'Time19_SerieA', 'Time20_SerieA'],
        'gols_mandante': [2, 1, 3, 0, 2, 1, 4, 0, 2, 1],
        'gols_visitante': [1, 1, 0, 2, 2, 0, 1, 0, 3, 2],
        'rodada': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        'pred_gols_mandante': [1.8, 1.2, 2.5, 0.9, 1.7, 1.5, 3.2, 0.8, 1.9, 1.3],
        'pred_gols_visitante': [0.9, 1.3, 0.7, 1.8, 1.6, 0.6, 1.1, 0.7, 2.5, 1.7]
    }
    
    # Criar dados de exemplo para Série B com odds
    serie_b_data = {
        'data': pd.date_range(start='2022-01-01', periods=10),
        'time_mandante': ['Time1_SerieB', 'Time2_SerieB', 'Time3_SerieB', 'Time4_SerieB', 'Time5_SerieB',
                         'Time6_SerieB', 'Time7_SerieB', 'Time8_SerieB', 'Time9_SerieB', 'Time10_SerieB'],
        'time_visitante': ['Time11_SerieB', 'Time12_SerieB', 'Time13_SerieB', 'Time14_SerieB', 'Time15_SerieB',
                          'Time16_SerieB', 'Time17_SerieB', 'Time18_SerieB', 'Time19_SerieB', 'Time20_SerieB'],
        'gols_mandante': [2, 1, 3, 0, 2, 1, 4, 0, 2, 1],
        'gols_visitante': [1, 1, 0, 2, 2, 0, 1, 0, 3, 2],
        'rodada': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        'odd_1': [1.8, 2.1, 1.5, 3.2, 2.0, 2.2, 1.4, 2.8, 2.1, 2.5],
        'odd_X': [3.5, 3.2, 4.0, 3.1, 3.3, 3.4, 4.5, 3.0, 3.2, 3.1],
        'odd_2': [4.2, 3.5, 6.0, 2.1, 3.7, 3.2, 7.0, 2.5, 3.4, 2.8],
        'odd_over_2_5': [1.9, 2.1, 1.8, 2.0, 1.9, 2.2, 1.7, 2.3, 1.8, 2.0],
        'odd_under_2_5': [1.9, 1.7, 2.0, 1.8, 1.9, 1.7, 2.1, 1.6, 2.0, 1.8],
        'prob_1_norm': [0.55, 0.47, 0.65, 0.30, 0.49, 0.45, 0.70, 0.35, 0.47, 0.39],
        'prob_X_norm': [0.28, 0.31, 0.24, 0.32, 0.30, 0.29, 0.22, 0.33, 0.31, 0.32],
        'prob_2_norm': [0.17, 0.22, 0.11, 0.38, 0.21, 0.26, 0.08, 0.32, 0.22, 0.29],
        'prob_over_2_5_norm': [0.52, 0.47, 0.55, 0.49, 0.52, 0.45, 0.58, 0.43, 0.55, 0.49],
        'prob_under_2_5_norm': [0.48, 0.53, 0.45, 0.51, 0.48, 0.55, 0.42, 0.57, 0.45, 0.51]
    }
    
    # Criar dados de exemplo para Série C com odds
    serie_c_data = {
        'data': pd.date_range(start='2022-01-01', periods=10),
        'time_mandante': ['Time1_SerieC', 'Time2_SerieC', 'Time3_SerieC', 'Time4_SerieC', 'Time5_SerieC',
                         'Time6_SerieC', 'Time7_SerieC', 'Time8_SerieC', 'Time9_SerieC', 'Time10_SerieC'],
        'time_visitante': ['Time11_SerieC', 'Time12_SerieC', 'Time13_SerieC', 'Time14_SerieC', 'Time15_SerieC',
                          'Time16_SerieC', 'Time17_SerieC', 'Time18_SerieC', 'Time19_SerieC', 'Time20_SerieC'],
        'gols_mandante': [2, 1, 3, 0, 2, 1, 4, 0, 2, 1],
        'gols_visitante': [1, 1, 0, 2, 2, 0, 1, 0, 3, 2],
        'rodada': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        'odd_1': [1.7, 2.0, 1.4, 3.0, 1.9, 2.1, 1.3, 2.7, 2.0, 2.4],
        'odd_X': [3.3, 3.0, 3.8, 3.0, 3.2, 3.3, 4.3, 2.9, 3.1, 3.0],
        'odd_2': [4.0, 3.3, 5.8, 2.0, 3.5, 3.0, 6.8, 2.4, 3.3, 2.7],
        'odd_over_2_5': [1.8, 2.0, 1.7, 1.9, 1.8, 2.1, 1.6, 2.2, 1.7, 1.9],
        'odd_under_2_5': [1.8, 1.6, 1.9, 1.7, 1.8, 1.6, 2.0, 1.5, 1.9, 1.7],
        'prob_1_norm': [0.58, 0.49, 0.68, 0.32, 0.51, 0.47, 0.73, 0.36, 0.49, 0.41],
        'prob_X_norm': [0.26, 0.29, 0.22, 0.30, 0.28, 0.27, 0.20, 0.31, 0.29, 0.30],
        'prob_2_norm': [0.16, 0.22, 0.10, 0.38, 0.21, 0.26, 0.07, 0.33, 0.22, 0.29],
        'prob_over_2_5_norm': [0.54, 0.49, 0.57, 0.51, 0.54, 0.47, 0.60, 0.45, 0.57, 0.51],
        'prob_under_2_5_norm': [0.46, 0.51, 0.43, 0.49, 0.46, 0.53, 0.40, 0.55, 0.43, 0.49]
    }
    
    return pd.DataFrame(serie_a_data), pd.DataFrame(serie_b_data), pd.DataFrame(serie_c_data)

# Criar dados de exemplo
df_serie_a, df_serie_b, df_serie_c = create_sample_data()

# Função para calcular EV (Expected Value)
def calculate_ev(prob, odd):
    """Calcula o Expected Value de uma aposta"""
    return (prob * odd) - 1

# Sidebar para filtros
st.sidebar.title("Filtros")

# Seleção de série
series_options = ["Série A", "Série B", "Série C"]
selected_serie = st.sidebar.selectbox("Selecione a Série", series_options)

# Selecionar o DataFrame correspondente à série escolhida
if selected_serie == "Série A":
    df = df_serie_a
    serie_label = "A"
elif selected_serie == "Série B":
    df = df_serie_b
    serie_label = "B"
else:  # Série C
    df = df_serie_c
    serie_label = "C"

# Filtros adicionais
# Lista de times únicos
times = sorted(list(set(df['time_mandante'].unique()) | set(df['time_visitante'].unique())))

# Filtro de time mandante
time_mandante = st.sidebar.selectbox("Time Mandante", ["Todos"] + times)
if time_mandante != "Todos":
    df = df[df['time_mandante'] == time_mandante]

# Filtro de time visitante
time_visitante = st.sidebar.selectbox("Time Visitante", ["Todos"] + times)
if time_visitante != "Todos":
    df = df[df['time_visitante'] == time_visitante]

# Filtro de rodada
rodadas = sorted(df['rodada'].unique())
selected_rodada = st.sidebar.selectbox("Rodada", ["Todas"] + list(rodadas))
if selected_rodada != "Todas":
    df = df[df['rodada'] == selected_rodada]

# Ordenamento quantitativo
st.sidebar.subheader("Ordenamento")

# Identificar colunas numéricas para ordenamento
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

# Adicionar opção para não ordenar
sort_column = st.sidebar.selectbox("Ordenar por", ["Sem ordenação"] + numeric_columns)

if sort_column != "Sem ordenação":
    sort_order = st.sidebar.radio("Ordem", ["Decrescente", "Crescente"])
    ascending = sort_order == "Crescente"
    df = df.sort_values(by=sort_column, ascending=ascending)

# Exibir dados
st.header(f"Dados do Campeonato Brasileiro {selected_serie}")

# Exibir tabela de dados
st.dataframe(df)

# Estatísticas básicas
st.subheader("Estatísticas Básicas")

col1, col2 = st.columns(2)

with col1:
    st.metric("Média de Gols Mandante", f"{df['gols_mandante'].mean():.2f}")
    if 'pred_gols_mandante' in df.columns:
        st.metric("Média de Gols Previstos (Mandante)", f"{df['pred_gols_mandante'].mean():.2f}")

with col2:
    st.metric("Média de Gols Visitante", f"{df['gols_visitante'].mean():.2f}")
    if 'pred_gols_visitante' in df.columns:
        st.metric("Média de Gols Previstos (Visitante)", f"{df['pred_gols_visitante'].mean():.2f}")

# Verificar se há odds disponíveis
if 'odd_1' in df.columns:
    st.subheader("Estatísticas de Odds")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Média Odd Vitória Mandante", f"{df['odd_1'].mean():.2f}")
    
    with col2:
        st.metric("Média Odd Empate", f"{df['odd_X'].mean():.2f}")
    
    with col3:
        st.metric("Média Odd Vitória Visitante", f"{df['odd_2'].mean():.2f}")

# Comparação entre odds e probabilidades com sinalização de EV+
if 'odd_1' in df.columns and 'prob_1_norm' in df.columns:
    st.subheader("Comparação entre Odds e Probabilidades (EV+)")
    
    # Calcular EV para cada mercado
    df['ev_1'] = df.apply(lambda row: calculate_ev(row['prob_1_norm'], row['odd_1']), axis=1)
    df['ev_X'] = df.apply(lambda row: calculate_ev(row['prob_X_norm'], row['odd_X']), axis=1)
    df['ev_2'] = df.apply(lambda row: calculate_ev(row['prob_2_norm'], row['odd_2']), axis=1)
    df['ev_over_2_5'] = df.apply(lambda row: calculate_ev(row['prob_over_2_5_norm'], row['odd_over_2_5']), axis=1)
    df['ev_under_2_5'] = df.apply(lambda row: calculate_ev(row['prob_under_2_5_norm'], row['odd_under_2_5']), axis=1)
    
    # Exibir tabela com EV
    st.write("### Tabela de Expected Value (EV+)")
    
    # Selecionar colunas relevantes para exibição
    display_columns = ['time_mandante', 'time_visitante', 'data', 'rodada',
                      'odd_1', 'odd_X', 'odd_2', 'odd_over_2_5', 'odd_under_2_5',
                      'prob_1_norm', 'prob_X_norm', 'prob_2_norm', 'prob_over_2_5_norm', 'prob_under_2_5_norm',
                      'ev_1', 'ev_X', 'ev_2', 'ev_over_2_5', 'ev_under_2_5']
    
    # Exibir DataFrame com EV
    st.dataframe(df[display_columns])
    
    # Destacar valores de EV positivos
    st.write("### Oportunidades com EV+ (Expected Value Positivo)")
    
    ev_positivo = df[(df['ev_1'] > 0) | (df['ev_X'] > 0) | (df['ev_2'] > 0) | 
                     (df['ev_over_2_5'] > 0) | (df['ev_under_2_5'] > 0)]
    
    if not ev_positivo.empty:
        st.dataframe(ev_positivo[display_columns])
    else:
        st.info("Não foram encontradas oportunidades com EV positivo nos dados filtrados.")

# Informações sobre o painel
st.markdown("---")
st.markdown("**Observações:**")
st.markdown("- Este painel demonstra a integração de dados das Séries A, B e C do Campeonato Brasileiro.")
st.markdown("- Os filtros permitem selecionar séries específicas, times e rodadas.")
st.markdown("- O ordenamento quantitativo permite classificar os dados por qualquer coluna numérica.")
st.markdown("- A análise de EV+ (Expected Value positivo) destaca oportunidades onde o valor esperado da aposta é positivo.")
st.markdown("- **Nota**: Esta versão usa dados de demonstração para garantir compatibilidade com o Streamlit Community Cloud.")
