import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd
import seaborn as sns
import time
import numpy as np

# st.set_page_config(layout='wide')
# Título e descrição do dashboard
st.title("Dashboard em Tempo Real")
st.subheader("Monitoramento de Temperatura e Consumo de Energia")

# Função para carregar dados do CSV
@st.cache_data(ttl=5)
def load_data():
    try:
        # Tenta carregar o CSV
        df = pd.read_csv('df_temperatura_energia.csv')
        df['Horario'] = pd.to_datetime(df['Horario'], format="%Y-%m-%d %H:%M:%S",errors='coerce')
        return df
    except FileNotFoundError:
        st.warning("O arquivo de dados ainda não foi gerado pelo servidor.")
        return pd.DataFrame(columns=['Horario', 'Tipo', 'Valor'])

# Dividindo a tela em duas colunas
col1, col2 = st.columns([3, 1])  # Ajustando a largura da coluna para gráficos e métricas

# Placeholder para os gráficos
graph_placeholder = col1.empty()
heatmap_placeholder = col1.empty()

# Placeholder para as métricas
metrics_placeholder = col2.empty()

# Loop para atualizar o dashboard
while True:
    df = load_data()
    if len(df)>2:
        if not df.empty:
            df_pivot = df.pivot(index='Horario', columns='Tipo', values='Valor').reset_index()

            fig, ax = plt.subplots(figsize=(8, 4))  # Reduzindo o tamanho do gráfico
            ax.plot(df_pivot['Horario'], df_pivot['Temperatura'], label='Temperatura', color='blue')
            ax.plot(df_pivot['Horario'], df_pivot['Energia'], label='Energia', color='green')
            
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) 
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            # Adicionando a grade apenas no eixo y com uma cor suave
            ax.yaxis.grid(True, color='lightgrey', linewidth=0.7)
            ax.xaxis.grid(False)
            # Configurações de estilo do gráfico
            # ax.set_xlabel("Horário")
            # ax.set_ylabel("Valores")
            
            # Configuração do eixo y para incrementos de 2.5, iniciando do 0
            ax.yaxis.set_major_locator(MultipleLocator(2.5))
            ax.set_ylim(bottom=0)
            # ax.set_title("Monitoramento de Temperatura e Energia ao Longo do Dia")
            ax.legend(loc='upper left', bbox_to_anchor=(0, 1.2))
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

            # Atualizando o gráfico no placeholder
            graph_placeholder.pyplot(fig)

            ## heatmap
            corr = df_pivot.corr()
            mask = np.triu(np.ones_like(corr, dtype=bool))

            f, ax = plt.subplots(figsize=(8, 4)) 
            sns.heatmap(corr, annot=True, fmt='.2f', vmin=0, vmax=1, cbar_kws={"shrink": 0.5},
                        annot_kws={"size": 12, "weight": 'bold', "color": 'black'})

            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.set_title("Correlação entre Temperatura Energia e Horas")
            plt.tight_layout()

            # Atualizando o heatmap no placeholder
            heatmap_placeholder.pyplot(f)

            # Cálculo das métricas para a coluna ao lado
            temp_max = df_pivot['Temperatura'].max()
            temp_min = df_pivot['Temperatura'].min()
            temp_mean = df_pivot['Temperatura'].mean()
            temp_std = df_pivot['Temperatura'].std()

            energia_max = df_pivot['Energia'].max()
            energia_min = df_pivot['Energia'].min()
            energia_mean = df_pivot['Energia'].mean()
            total = df_pivot['Energia'].sum()

            # Formatação da mensagem com as métricas
            metrics_message = metrics_message = f"""
                                                <h4>Temperatura:</h4>\n
                                                - Máxima: {temp_max:.2f} °C
                                                - Mínima: {temp_min:.2f} °C
                                                - Média: {temp_mean:.2f} °C
                                                - DP: {temp_std:.2f} °C
                                                
                                                
                                                <h4>Consumo de Energia:</h4>\n
                                                - Máximo: {energia_max:.2f} kWh
                                                - Mínimo: {energia_min:.2f} kWh
                                                - Média: {energia_mean:.2f} kWh
                                                - Total: {total:.2f} KWh
                                                """

            with metrics_placeholder:
                metrics_placeholder.markdown(metrics_message, unsafe_allow_html=True)

        else:
            st.write("Aguardando dados do servidor...")

        # Intervalo de atualização
        time.sleep(5)
        







