import polars as pl
import plotly.graph_objects as go

def plot_local_votacao(dataset, candidato=False):
    # Agrupamento por local de votação e soma da quantidade de votos
    votos_por_local = dataset.group_by('NM_LOCAL_VOTACAO').agg(pl.sum('QT_VOTOS')).sort('QT_VOTOS', descending=True)
    # definição de titulo caso a função seja exclusiva para um unico candidato
    title='Locais de Votação'
    if candidato:
        title='Locais o candidato obteve votos'
    # Gráfico de barras dos locais de votação com mais votos
    fig = go.Figure(data=[go.Bar(
        x=votos_por_local['NM_LOCAL_VOTACAO'],
        y=votos_por_local['QT_VOTOS'],
        marker_color='skyblue'
    )])

    fig.update_layout(
        title=title,
        xaxis=dict(title=''),
        yaxis=dict(title='Quantidade de Votos'),
        xaxis_tickangle=-90
    )
    return fig


def table_prop(dataset_municipio, dataset_candidato):
    grouped1 = dataset_municipio.group_by('NM_LOCAL_VOTACAO').agg(pl.sum('QT_VOTOS').alias('TOTAL DE VOTOS'))
    grouped2 = dataset_candidato.group_by('NM_LOCAL_VOTACAO').agg(pl.sum('QT_VOTOS').alias('VOTOS DO CANDIDATO'))
    joined = grouped1.join(grouped2, on='NM_LOCAL_VOTACAO', how='inner')

    joined = joined.with_columns([(joined['VOTOS DO CANDIDATO'] / joined['TOTAL DE VOTOS'] * 100).alias('PORCENTAGEM DOS VOTOS')])
    
    joined.rename({"NM_LOCAL_VOTACAO": "LOCAL DE VOTACAO"})

    return joined.sort('TOTAL DE VOTOS', descending=True)



# As funções "plot_local_candicato", "plot_local_candicato_pie" funciona de maneira similar a "plot_local_votacao"
def plot_local_candicato(dataset, max=False, min=False):
    votos_por_candidato = dataset.group_by('NM_VOTAVEL').agg(pl.sum('QT_VOTOS')).sort('QT_VOTOS', descending=True)
    title = 'Candidatos'
    marker_color='salmon'
    if max:
        votos_por_candidato = votos_por_candidato.head(10)
        title = 'Dez candidatos mais votados' 
        marker_color = 'seagreen'
    if min:
        votos_por_candidato = dataset.group_by('NM_VOTAVEL').agg(pl.sum('QT_VOTOS')).sort('QT_VOTOS', descending=False)
        votos_por_candidato = votos_por_candidato.head(10).sort('QT_VOTOS', descending=True)
        title = 'Dez candidatos menos votados'
        marker_color = 'sandybrown'

    fig = go.Figure(data=[go.Bar(
        x=votos_por_candidato['NM_VOTAVEL'],
        y=votos_por_candidato['QT_VOTOS'],
        marker_color=marker_color
    )])

    fig.update_layout(
        title=title,
        xaxis=dict(title=''),
        yaxis=dict(title='Quantidade de Votos'),
        xaxis_tickangle=-90
    )

    return fig

def plot_local_candicato_pie(dataset):
    votos_por_candidato = dataset.group_by('NM_VOTAVEL').agg(pl.sum('QT_VOTOS')).sort('QT_VOTOS', descending=True)
    total_votos = votos_por_candidato['QT_VOTOS'].sum()
    proporcao_votos = votos_por_candidato['QT_VOTOS'] / total_votos
    votos_por_candidato = votos_por_candidato.with_columns(pl.lit('Proporção'), proporcao_votos)
    fig = go.Figure(data=[go.Pie(labels=votos_por_candidato['NM_VOTAVEL'], values=votos_por_candidato['QT_VOTOS'], hole=.3)])

    return fig