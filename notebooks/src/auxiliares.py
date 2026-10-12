import re
import time
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

from .config import N_ESTUDIOS


def extrair_ano(aired):
    return aired.str.extract(r"(\d{4})")[0].astype(float)


def faixa_de_ano(ano):
    return pd.cut(
        ano,
        bins=[0, 2000, 2010, 2015, 2030],
        labels=["Até 2000", "2000-2010", "2010-2015", "2015-2030"],
    )


def tamanho(episodios):
    episodios = pd.to_numeric(episodios, errors="coerce")
    return pd.cut(
        episodios,
        bins=[0, 1, 13, 26, np.inf],
        labels=["1 episódio", "2-13 episódios", "14-26 episódios", "27+ episódios"],
    )


def dummies_multiplos(coluna, prefixo, manter=None):
    dummies = coluna.str.get_dummies(sep=", ").drop(columns="Unknown", errors="ignore")
    if manter is not None:
        dummies = dummies[manter]
    return dummies.add_prefix(f"{prefixo}: ")


def montar_features(df):
    """Variáveis do K-means: dummies + popularidade (única variável de popularidade)."""
    top_estudios = (
        df["Studios"].str.split(", ").explode().loc[lambda s: s != "Unknown"]
        .value_counts().head(N_ESTUDIOS).index.tolist()
    )
    simples = pd.get_dummies(
        df[["Type", "Source", "Rating", "Faixa de ano", "Tamanho"]].replace("Unknown", np.nan),
        prefix=["Tipo", "Fonte", "Classificação", "Ano", "Tamanho"],
        prefix_sep=": ",
        dtype=int,
    )
    return pd.concat(
        [
            dummies_multiplos(df["Genres"], "Gênero"),
            dummies_multiplos(df["Studios"], "Estúdio", manter=top_estudios),
            simples,
            df[["Popularity"]],
        ],
        axis=1,
    )


def _abrir(url):
    return urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()


def baixar_capa(mal_id, pasta):
    """Baixa a capa do anime da página do MyAnimeList, se ainda não estiver na pasta."""
    destino = pasta / f"{mal_id}.jpg"
    if not destino.exists():
        pagina = _abrir(f"https://myanimelist.net/anime/{mal_id}").decode("utf-8", "ignore")
        url = re.search(r'property="og:image" content="([^"]+)"', pagina).group(1)
        destino.write_bytes(_abrir(url))
        time.sleep(1)
    return destino
