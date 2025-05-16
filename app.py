import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from scipy import stats

# Configuração da página
st.set_page_config(layout="wide", page_title="Sistema de Previsão de Futebol - Brasileirão")

# Título e descrição
st.title("Sistema de Previsão de Partidas de Futebol")
st.subheader("Campeonato Brasileiro - Séries A, B e C")

# Função para carregar dados
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Arquivo de dados não encontrado: {file_path}. Verifique se o arquivo está no mesmo diretório que o app.py no repositório GitHub e se o nome está correto.")
        return pd.DataFrame()

# Função para calcular EV (Expected Value)
def calculate_ev(prob, odd):
    """Calcula o Expected Value de uma aposta"""
    return (prob * odd) - 1

# Função para criar gráfico de regressão à média
def plot_regression_to_mean(df, x_col, y_col, title):
    """Cria um gráfico de regressão à média para duas variáveis"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotar os pontos
    sns.scatterplot(x=df[x_col], y=df[y_col], alpha=0.6, ax=ax)
    
    # Calcular a linha de regressão
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[x_col], df[y_col])
    x_line = np.linspace(df[x_col].min(), df[x_col].max(), 100)
    y_line = slope * x_line + intercept
    
    # Plotar a linha de regressão
    plt.plot(x_line, y_line, color='red', linestyle='--')
    
    # Plotar a linha de média (regressão perfeita à média)
    mean_y = df[y_col].mean()
    plt.axhline(y=mean_y, color='green', linestyle='-.')
    
    # Adicionar informações da regressão
    plt.text(0.05, 0.95, f'R² = {r_value**2:.3f}\nSlope = {slope:.3f}', 
             transform=ax.transAxes, fontsize=12, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))
    
    # Configurar o gráfico
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    return fig

# Carregar dados das três séries
serie_a_path = "serie_a_padronizada.csv"
serie_b_path = "serie_b_com_odds.csv"
serie_c_path = "serie_c_com_odds.csv"

df_serie_a = load_data(serie_a_path)
df_serie_b = load_data(serie_b_path)
df_serie_c = load_data(serie_c_path)

# Verificar se os dados foram carregados
series_loaded = {
    "Série A": not df_serie_a.empty,
    "Série B": not df_serie_b.empty,
    "Série C": not df_serie_c.empty
}

# Sidebar para filtros
st.sidebar.title("Filtros")

# Seleção de série
series_options = [serie for serie, loaded in series_loaded.items() if loaded]
if series_options:
    selected_serie = st.sidebar.selectbox("Selecione a Série", series_options)
else:
    st.warning("Nenhum dado de série foi carregado. Verifique se os arquivos estão presentes no repositório.")
    st.stop()

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

# Converter coluna de data para datetime se existir
if 'data' in df.columns:
    df['data'] = pd.to_datetime(df['data'])

# Filtros adicionais
if 'time_mandante' in df.columns and 'time_visitante' in df.columns:
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

# Filtro de rodada se existir
if 'rodada' in df.columns:
    rodadas = sorted(df['rodada'].unique())
    selected_rodada = st.sidebar.selectbox("Rodada", ["Todas"] + list(rodadas))
    if selected_rodada != "Todas":
        df = df[df['rodada'] == selected_rodada]

# Ordenamento quantitativo
if not df.empty:
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

# Verificar se há dados após aplicação dos filtros
if df.empty:
    st.warning("Não há dados disponíveis com os filtros selecionados.")
else:
    # Exibir tabela de dados
    st.dataframe(df)
    
    # Estatísticas básicas
    st.subheader("Estatísticas Básicas")
    
    col1, col2 = st.columns(2)
    
    # Verificar colunas disponíveis para estatísticas
    if 'gols_mandante' in df.columns and 'gols_visitante' in df.columns:
        with col1:
            st.metric("Média de Gols Mandante", f"{df['gols_mandante'].mean():.2f}")
            if 'pred_gols_mandante' in df.columns:
                st.metric("Média de Gols Previstos (Mandante)", f"{df['pred_gols_mandante'].mean():.2f}")
        
        with col2:
            st.metric("Média de Gols Visitante", f"{df['gols_visitante'].mean():.2f}")
            if 'pred_gols_visitante' in df.columns:
                st.metric("Média de Gols Previstos (Visitante)", f"{df['pred_gols_visitante'].mean():.2f}")
    
    # Verificar se há odds disponíveis
    odds_columns = [col for col in df.columns if col.startswith('odd_')]
    if odds_columns:
        st.subheader("Estatísticas de Odds")
        
        col1, col2, col3 = st.columns(3)
        
        if 'odd_1' in df.columns:
            with col1:
                st.metric("Média Odd Vitória Mandante", f"{df['odd_1'].mean():.2f}")
        
        if 'odd_X' in df.columns:
            with col2:
                st.metric("Média Odd Empate", f"{df['odd_X'].mean():.2f}")
        
        if 'odd_2' in df.columns:
            with col3:
                st.metric("Média Odd Vitória Visitante", f"{df['odd_2'].mean():.2f}")
    
    # Gráficos de desempenho com regressão à média
    st.subheader("Gráficos de Desempenho com Regressão à Média")
    
    # Verificar se existem colunas para gráficos de regressão
    if 'gols_mandante' in df.columns and 'pred_gols_mandante' in df.columns:
        st.write("### Regressão à Média - Gols Mandante")
        fig_mandante = plot_regression_to_mean(
            df, 
            'pred_gols_mandante', 
            'gols_mandante', 
            f'Regressão à Média: Gols Previstos vs Reais (Mandante) - {selected_serie}'
        )
        st.pyplot(fig_mandante)
    
    if 'gols_visitante' in df.columns and 'pred_gols_visitante' in df.columns:
        st.write("### Regressão à Média - Gols Visitante")
        fig_visitante = plot_regression_to_mean(
            df, 
            'pred_gols_visitante', 
            'gols_visitante', 
            f'Regressão à Média: Gols Previstos vs Reais (Visitante) - {selected_serie}'
        )
        st.pyplot(fig_visitante)
    
    # Comparação entre odds e probabilidades com sinalização de EV+
    if 'odd_1' in df.columns and 'prob_1_norm' in df.columns:
        st.subheader("Comparação entre Odds e Probabilidades (EV+)")
        
        # Calcular EV para cada mercado
        if 'prob_1_norm' in df.columns and 'odd_1' in df.columns:
            df['ev_1'] = df.apply(lambda row: calculate_ev(row['prob_1_norm'], row['odd_1']), axis=1)
        
        if 'prob_X_norm' in df.columns and 'odd_X' in df.columns:
            df['ev_X'] = df.apply(lambda row: calculate_ev(row['prob_X_norm'], row['odd_X']), axis=1)
        
        if 'prob_2_norm' in df.columns and 'odd_2' in df.columns:
            df['ev_2'] = df.apply(lambda row: calculate_ev(row['prob_2_norm'], row['odd_2']), axis=1)
        
        if 'prob_over_2_5_norm' in df.columns and 'odd_over_2_5' in df.columns:
            df['ev_over_2_5'] = df.apply(lambda row: calculate_ev(row['prob_over_2_5_norm'], row['odd_over_2_5']), axis=1)
        
        if 'prob_under_2_5_norm' in df.columns and 'odd_under_2_5' in df.columns:
            df['ev_under_2_5'] = df.apply(lambda row: calculate_ev(row['prob_under_2_5_norm'], row['odd_under_2_5']), axis=1)
        
        # Exibir tabela com EV
        ev_columns = [col for col in df.columns if col.startswith('ev_')]
        if ev_columns:
            st.write("### Tabela de Expected Value (EV+)")
            
            # Selecionar colunas relevantes para exibição
            display_columns = ['time_mandante', 'time_visitante', 'data', 'rodada'] + \
                             [col for col in df.columns if col.startswith('odd_')] + \
                             [col for col in df.columns if col.startswith('prob_')] + \
                             ev_columns
            
            # Filtrar apenas colunas que existem no DataFrame
            display_columns = [col for col in display_columns if col in df.columns]
            
            # Destacar EV positivo
            def highlight_positive_ev(val):
                if isinstance(val, (int, float)) and val > 0 and str(val).startswith('ev_'):
                    return 'background-color: lightgreen'
                return ''
            
            # Exibir DataFrame com EV destacado
            st.dataframe(df[display_columns].style.applymap(highlight_positive_ev, subset=ev_columns))
            
            # Gráfico de distribuição de EV
            st.write("### Distribuição de Expected Value (EV)")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            for ev_col in ev_columns:
                if ev_col in df.columns:
                    market_name = ev_col.replace('ev_', '')
                    sns.kdeplot(df[ev_col].dropna(), label=f'EV {market_name}', ax=ax)
            
            plt.axvline(x=0, color='red', linestyle='--', label='EV = 0 (Breakeven)')
            plt.title(f'Distribuição de Expected Value por Mercado - {selected_serie}')
            plt.xlabel('Expected Value (EV)')
            plt.ylabel('Densidade')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            
            st.pyplot(fig)

# Informações sobre o painel
st.markdown("---")
st.markdown("**Observações:**")
st.markdown("- Este painel integra dados das Séries A, B e C do Campeonato Brasileiro.")
st.markdown("- Os filtros permitem selecionar séries específicas, times e rodadas.")
st.markdown("- O ordenamento quantitativo permite classificar os dados por qualquer coluna numérica.")
st.markdown("- Os gráficos de regressão à média mostram a relação entre valores previstos e reais, indicando tendência de regressão.")
st.markdown("- A análise de EV+ (Expected Value positivo) destaca oportunidades onde o valor esperado da aposta é positivo.")
