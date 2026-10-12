import pandas as pd
import plotly.express as px
import streamlit as st
from joblib import load

from notebooks.src.config import (
    ANIMES_CLUSTERS,
    MATRIZ_USUARIO_ANIME,
    MAX_PERSONAS,
    METRICAS,
    METRICAS_DISTANCIA,
    PASTA_CAPAS,
)
from notebooks.src.graficos import AZUL, ROTULOS
from notebooks.src.models import ajustar_vizinhos, montar_vetores, recomendar_por_usuarios

CINZA_CLARO = "#d9d8d4"

st.set_page_config(page_title="Recomendação de animes", page_icon="🎌", layout="wide")


@st.cache_data
def carregar_animes():
    return pd.read_parquet(ANIMES_CLUSTERS)


@st.cache_resource
def carregar_matriz():
    return load(MATRIZ_USUARIO_ANIME)


@st.cache_resource
def carregar_vizinhos(metrica):
    return ajustar_vizinhos(carregar_matriz(), metrica)


@st.cache_data
def carregar_metricas():
    return pd.read_csv(METRICAS, index_col="Modelo")


def grafico_barras(serie, formato):
    serie = serie.dropna().sort_values()
    fig = px.bar(x=serie.values, y=serie.index, orientation="h", text=serie.map(formato.format))
    fig.update_traces(marker_color=AZUL, textposition="outside", hovertemplate="%{y}: %{text}<extra></extra>")
    fig.update_layout(
        height=60 + 40 * len(serie), margin=dict(l=0, r=40, t=10, b=0),
        xaxis=dict(visible=False), yaxis_title=None,
    )
    return fig


animes = carregar_animes()
matriz = carregar_matriz()
personas = animes[animes["Persona"]].sort_values("Popularity")

st.title("Recomendação de animes")
st.caption(
    "Filtragem colaborativa baseada em usuários para quem ainda não tem histórico (cold start). "
    "TCC da Especialização em Data Science & Big Data — UFPR."
)

aba_recomendar, aba_clusters, aba_avaliacao = st.tabs(["Recomendações", "Clusters", "Avaliação"])

with aba_recomendar:
    st.subheader("1. Escolha até 3 animes de que você gosta")
    st.write("Cada anime representa um dos 20 grupos (personas) encontrados pelo K-means.")
    escolhidos = []
    for inicio in range(0, len(personas), 5):
        for coluna, anime in zip(st.columns(5), personas.iloc[inicio : inicio + 5].itertuples()):
            with coluna:
                st.image(str(PASTA_CAPAS / f"{anime.MAL_ID}.jpg"), width="stretch")
                if st.checkbox(anime.Name, key=f"persona_{anime.MAL_ID}"):
                    escolhidos.append(anime.Name)

    st.subheader("2. Escolha a distância")
    metrica = st.radio(
        "Distância", METRICAS_DISTANCIA, format_func=ROTULOS.get, horizontal=True,
        label_visibility="collapsed",
        help="Como medir a semelhança entre você e os outros usuários. Cosine teve o melhor resultado na avaliação.",
    )

    st.subheader("3. Recomendações")
    if not escolhidos:
        st.info("Selecione pelo menos um anime acima.")
    elif len(escolhidos) > MAX_PERSONAS:
        st.warning(f"Selecione no máximo {MAX_PERSONAS} animes.")
    else:
        indices = animes.index[animes["Name"].isin(escolhidos)].tolist()
        vetor = montar_vetores([indices], n_animes=matriz.shape[1])
        recomendados = recomendar_por_usuarios(carregar_vizinhos(metrica), matriz, vetor)[0]

        for posicao, anime in enumerate(animes.loc[recomendados].itertuples(), start=1):
            ano = "" if pd.isna(anime.Ano) else f" · {anime.Ano:.0f}"
            with st.expander(f"**{posicao}. {anime.Name}** — {anime.Type}{ano} · nota {anime.Score}"):
                st.caption(anime.Genres)
                st.write(anime.Sinopse if isinstance(anime.Sinopse, str) else "Sem sinopse.")
                st.link_button("Ver no MyAnimeList", f"https://myanimelist.net/anime/{anime.MAL_ID}")

with aba_clusters:
    st.subheader("Os 20 clusters de animes")
    st.write(
        "Cada ponto é um anime, posicionado pelos 2 componentes principais (PCA) das suas características. "
        "Escolha um cluster para destacá-lo."
    )
    opcoes = personas.sort_values("Cluster")
    cluster = st.selectbox(
        "Cluster",
        opcoes["Cluster"],
        format_func=lambda c: f"{c} — {opcoes.set_index('Cluster').loc[c, 'Name']}",
    )
    do_cluster = animes["Cluster"] == cluster
    st.caption(f"Características que mais se destacam: {animes.loc[do_cluster, 'Descrição do cluster'].iloc[0]}")

    coluna_grafico, coluna_lista = st.columns([3, 2])
    with coluna_grafico:
        dados = animes.assign(Grupo=do_cluster.map({True: f"Cluster {cluster}", False: "Outros"})).sort_values("Grupo", ascending=False)
        fig = px.scatter(
            dados, x="PCA 1", y="PCA 2", color="Grupo", hover_name="Name",
            hover_data={"Genres": True, "PCA 1": False, "PCA 2": False, "Grupo": False},
            color_discrete_map={f"Cluster {cluster}": AZUL, "Outros": CINZA_CLARO},
        )
        fig.update_traces(marker_size=5)
        fig.update_layout(height=520, legend_title=None, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, width="stretch")
    with coluna_lista:
        st.write(f"**{do_cluster.sum()} animes** — os mais populares:")
        st.dataframe(
            animes[do_cluster].nsmallest(15, "Popularity")[["Name", "Type", "Genres"]],
            hide_index=True, width="stretch", height=480,
        )

with aba_avaliacao:
    metricas = carregar_metricas()
    st.subheader("Como os modelos se saíram")
    coluna_hit, coluna_serendipity = st.columns(2)
    with coluna_hit:
        st.markdown("**Hit Rate** — maior é melhor")
        st.caption("Escondemos um anime nota 10 de cada usuário de teste. É hit se ele aparece entre as 10 recomendações.")
        st.plotly_chart(grafico_barras(metricas["Hit Rate"], "{:.1%}"), width="stretch")
    with coluna_serendipity:
        st.markdown("**Serendipity** — menor é melhor")
        st.caption("Fração das recomendações que está no Top 10 de animes mais populares, em todas as combinações de até 3 personas.")
        st.plotly_chart(grafico_barras(metricas["Serendipity"], "{:.1%}"), width="stretch")
    st.write(
        "A distância **Cosine** teve o melhor resultado nas duas métricas. "
        "Os detalhes estão no notebook `04_avaliacao.ipynb`."
    )
