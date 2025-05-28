import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard Balança e Água", layout="wide")

@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv('dados_balanca_agua.csv')
        
        # Converte colunas
        df['DataHora'] = pd.to_datetime(df['DataHora'])
        df['Peso_g'] = pd.to_numeric(df['Peso_g']).round(1)
        df['AguaPresente'] = df['AguaPresente'].astype(int)
        
        # Calcula tempo decorrido
        df['TempoDecorrido'] = (df['DataHora'] - df['DataHora'].min()).dt.total_seconds()
        
        return df.sort_values('DataHora')
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def main():
    st.title("Monitoramento em Tempo Real - Balança e Sensor de Água")
    
    df = load_data()
    
    if df.empty:
        st.warning("Aguardando dados...")
        return
    
    with st.sidebar:
        st.header("Filtros")
        min_time = df['TempoDecorrido'].min()
        max_time = df['TempoDecorrido'].max()
        time_range = st.slider(
            "Intervalo de Tempo (segundos)",
            min_value=min_time,
            max_value=max_time,
            value=(min_time, max_time)
        )
        
        filtered_df = df[
            (df['TempoDecorrido'] >= time_range[0]) & 
            (df['TempoDecorrido'] <= time_range[1])
        ]

    col1, col2, col3 = st.columns(3)
    with col1:
        peso_medio = filtered_df['Peso_g'].mean().round(1)
        st.metric("Peso Médio", f"{peso_medio:.1f} g")
    with col2:
        st.metric("Tempo com Água", f"{filtered_df['AguaPresente'].sum() * 1.5:.1f} s")
    with col3:
        st.metric("Última Atualização", df['DataHora'].max().strftime('%H:%M:%S'))

    tab1, tab2, tab3 = st.tabs(["Peso", "Água", "Maiores Pesos"])
    
    with tab1:
        fig_peso = px.line(
            filtered_df,
            x='DataHora',
            y='Peso_g',
            title='Variação de Peso',
            labels={'Peso_g': 'Peso (g)', 'DataHora': 'Horário'}
        )
        fig_peso.update_layout(yaxis_tickformat='.1f')
        st.plotly_chart(fig_peso, use_container_width=True)
    
    with tab2:
        fig_agua = px.bar(
            filtered_df,
            x='DataHora',
            y='AguaPresente',
            title='Presença de Água',
            labels={'AguaPresente': 'Água Detectada', 'DataHora': 'Horário'}
        )
        st.plotly_chart(fig_agua, use_container_width=True)
    
    with tab3:
        st.subheader("Top 10 Maiores Pesos Detectados")
        top_pesos = df.nlargest(10, 'Peso_g')[['DataHora', 'Peso_g']].copy()
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(
                top_pesos,
                column_config={
                    "DataHora": "Horário",
                    "Peso_g": st.column_config.NumberColumn("Peso", format="%.1f g")
                },
                hide_index=True
            )
        
        with col2:
            fig_top = px.bar(
                top_pesos,
                x='DataHora',
                y='Peso_g',
                text=top_pesos['Peso_g'].round(1).astype(str) + ' g',
                labels={'Peso_g': 'Peso (g)', 'DataHora': 'Horário'}
            )
            fig_top.update_traces(textposition='outside')
            fig_top.update_layout(yaxis_tickformat='.1f')
            st.plotly_chart(fig_top, use_container_width=True)

    with st.expander("Visualizar Dados Brutos"):
        st.dataframe(df)

if __name__ == "__main__":
    main()