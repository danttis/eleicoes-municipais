import streamlit as st
import plotly.express as px
from funcoes import *

st.set_page_config(page_title="Dashboard de Análise Votos", page_icon=":rocket:", layout="wide", initial_sidebar_state="expanded")

data = pl.read_csv('./votacao_secao_2020_CE.csv', separator=';', encoding='Latin-1') # https://dadosabertos.tse.jus.br/dataset/resultados-2020

ano = data['ANO_ELEICAO'].unique()[0]
st.title(f'Análise dos dados eleitorais de {ano}')

st.sidebar.title('Menu')

filtro_principal_municipio = st.sidebar.selectbox("Selecione o Município", ['Selecione'] + data['NM_MUNICIPIO'].unique().sort().to_list())

if filtro_principal_municipio != 'Selecione':
    data =  data.filter(data['NM_MUNICIPIO'] == filtro_principal_municipio)
    
    filtro_secundario_votos = st.sidebar.selectbox("Selecione o filtro", ['Selecione','Cargo', 'Candidato'])

    if filtro_secundario_votos != 'Selecione':
        if filtro_secundario_votos == 'Cargo':
            filtro_cargo = st.sidebar.selectbox("Selecione o Cargo", ['Prefeito','Vereador'])
            if filtro_cargo == 'Prefeito':
                data = data.filter(data['DS_CARGO'] == 'Prefeito')
                data_eleicoes = data['DT_ELEICAO'].str.to_date()
                data = data.with_columns(data_eleicoes.alias('DT_ELEICAO'))
                if len(data['DT_ELEICAO'].unique()) == 1:
                    data_turno = data['DT_ELEICAO'].unique()[0]
                    st.title(f'Votação para Prefeito de {filtro_principal_municipio}: eleição de apenas um turno \n Data: {data_turno}')
                    col1,col2 = st.columns(2)
                    col1.plotly_chart(plot_local_candicato(data))
                    col2.plotly_chart(plot_local_candicato_pie(data))
                    st.plotly_chart(plot_local_votacao(data))
                else:
                    data_turnos = data['DT_ELEICAO'].unique().sort()

                    primeiro, segundo = data_turnos[0], data_turnos[1]
                    data1 = data.filter(data['DT_ELEICAO'] == primeiro)
                    st.title(f'Votação para Prefeito de {filtro_principal_municipio}: :blue[1º] turno \n Data: {primeiro}')
                    col1,col2 = st.columns(2)
                    col1.plotly_chart(plot_local_candicato(data1))
                    col2.plotly_chart(plot_local_candicato_pie(data1))
                    st.plotly_chart(plot_local_votacao(data1))
                    data2 = data.filter(data['DT_ELEICAO'] == segundo)
                    st.title(f'Votação para Prefeito de {filtro_principal_municipio}: :red[2º] turno \n Data: {segundo}')
                    col3, col4 = st.columns(2)
                    col3.plotly_chart(plot_local_candicato(data2))
                    col4.plotly_chart(plot_local_candicato_pie(data2))
                    st.plotly_chart(plot_local_votacao(data2))

            else:
                 data = data.filter(data['DS_CARGO'] == 'Vereador')
                 st.title(f'Votação para Vereadores de {filtro_principal_municipio}')
                 st.plotly_chart(plot_local_candicato(data))
                 col1,col2 = st.columns(2)
                 col1.plotly_chart(plot_local_candicato(data,max=True))
                 col2.plotly_chart(plot_local_candicato(data,min=True))
                 st.plotly_chart(plot_local_votacao(data))
        else:
            filtro_candidato = st.sidebar.selectbox("Selecione o Candidato", ['Selecione'] + data['NM_VOTAVEL'].unique().sort().to_list())
            if filtro_candidato != 'Selecione':
                data1 = data.filter(data['NM_VOTAVEL'] == filtro_candidato)
                cargo = data1['DS_CARGO'].unique()[0]
                st.title(f'Candidato a {cargo}:{filtro_candidato}')
                col1,col2 = st.columns(2)
                quantidade_candidato = sum(data1['QT_VOTOS'])
                data = data.filter(data['DS_CARGO'] == 'Prefeito')
                quantidade_total = sum(data['QT_VOTOS'])
                proporcao_de_votos = quantidade_candidato/quantidade_total *100
                col1.html(f'<table style="border-collapse: collapse; width: 100%; border: 1px solid black;"><tr><td style="border: 1px solid black; padding: 8px;">Total de Votos</td><td style="border: 1px solid black; padding: 8px;">Votos do Candidato</td><td style="border: 1px solid black; padding: 8px;">Percentual de votos do candidato</td></tr><tr><td style="border: 1px solid black; padding: 8px;">{quantidade_total}</td><td style="border: 1px solid black; padding: 8px;">{quantidade_candidato}</td><td style="border: 1px solid black; padding: 8px;">{round(proporcao_de_votos,2)}%</td></tr></table>')
                col2.plotly_chart(plot_local_votacao(data1, candidato=True))
                tableP = table_prop(data, data1)
                col1.text("Percentual de votos do candidato por local")
                col1.dataframe(tableP)
                





