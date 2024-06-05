from funcoes import *

st.set_page_config(page_title="Dashboard de Análise Votos", page_icon=":rocket:", layout="wide", initial_sidebar_state="expanded")

data = pl.read_csv('./votacao_secao_2020_CE.csv', separator=';', encoding='Latin-1') # https://dadosabertos.tse.jus.br/dataset/resultados-2020

ano = data['ANO_ELEICAO'].unique()[0]
st.title(f'Análise dos dados eleitorais de {ano} - CE')
st.sidebar.title('Menu')
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://uploaddeimagens.com.br/images/004/793/299/full/fundo.png");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)


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
                if filtro_candidato == 'VOTO BRANCO' or filtro_candidato == 'VOTO NULO':
                    filtro_cargoNB = st.sidebar.selectbox("Selecione o Cargo", ['Prefeito','Vereador'])
                    data1 = data.filter((data['NM_VOTAVEL'] == filtro_candidato) & (data['DS_CARGO'] == filtro_cargoNB))
                else: 
                    data1 = data.filter(data['NM_VOTAVEL'] == filtro_candidato)
                if len(data1['DT_ELEICAO'].unique()) == 1:
                    primeiro = data['DT_ELEICAO'].unique()[0]
                    data = data.filter(data['DT_ELEICAO'] == primeiro)
                    plot_estatisticas_candidato(data, data1, filtro_candidato=filtro_candidato)
                else:
                    data_turnos = data['DT_ELEICAO'].unique().sort()
                    primeiro, segundo = data_turnos[0], data_turnos[1]
                    data1_turno1 = data1.filter(data1['DT_ELEICAO'] == primeiro)
                    data1_turno2 = data1.filter(data1['DT_ELEICAO'] == segundo)
                    
                    data3 = data.filter(data['DT_ELEICAO'] == primeiro)
                    data4 = data.filter(data['DT_ELEICAO'] == segundo)
                    plot_estatisticas_candidato(data3, data1_turno1, filtro_candidato=filtro_candidato, cargo='Prefeito')
                    plot_estatisticas_candidato(data4, data1_turno2, filtro_candidato=filtro_candidato, turno=2, cargo='Prefeito')
                
                





