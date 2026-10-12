from itertools import combinations

import numpy as np
from scipy import sparse
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

from .config import K_VIZINHOS, N_RECOMENDACOES


def montar_vetores(escolhas, n_animes, nota=10):
    """Um usuário novo por linha: nota máxima nos animes escolhidos, zero no resto."""
    linhas = np.repeat(np.arange(len(escolhas)), [len(e) for e in escolhas])
    colunas = np.concatenate([np.asarray(e) for e in escolhas])
    dados = np.full(len(colunas), nota, dtype=np.float32)
    return sparse.csr_matrix((dados, (linhas, colunas)), shape=(len(escolhas), n_animes))


def combinacoes_de_personas(animes_persona, maximo):
    return [
        list(c)
        for tamanho in range(1, maximo + 1)
        for c in combinations(animes_persona, tamanho)
    ]


def _top_n(pontuacoes, vistos, n):
    pontuacoes = np.asarray(pontuacoes, dtype=np.float64).ravel()
    pontuacoes[vistos] = -np.inf
    top = np.argpartition(-pontuacoes, n)[:n]
    return top[np.argsort(-pontuacoes[top], kind="stable")]


def ajustar_vizinhos(matriz, metrica):
    return NearestNeighbors(metric=metrica, algorithm="brute", n_jobs=-1).fit(matriz)


def recomendar_por_usuarios(knn, matriz, vetores, k=K_VIZINHOS, n=N_RECOMENDACOES):
    """Filtragem colaborativa baseada em usuários.

    Busca os k usuários mais próximos de cada vetor e recomenda os animes com a
    maior soma de notas entre esses vizinhos, ignorando os que o usuário já viu.
    """
    vizinhos = knn.kneighbors(vetores, n_neighbors=k, return_distance=False)
    return np.array(
        [
            _top_n(matriz[vizinhos[i]].sum(axis=0), vetores[i].indices, n)
            for i in range(vetores.shape[0])
        ]
    )


def similaridade_entre_animes(matriz):
    colunas = normalize(matriz.T.astype(np.float32))
    return (colunas @ colunas.T).toarray()


def recomendar_por_itens(similaridade, vetores, n=N_RECOMENDACOES):
    """Baseline item-based: animes mais parecidos (cosseno) com os já avaliados."""
    pontuacoes = vetores @ similaridade
    return np.array(
        [_top_n(pontuacoes[i], vetores[i].indices, n) for i in range(vetores.shape[0])]
    )


def recomendar_populares(matriz, vetores, n=N_RECOMENDACOES):
    """Baseline: os n animes mais avaliados que o usuário ainda não viu."""
    popularidade = matriz.getnnz(axis=0)
    return np.array(
        [_top_n(popularidade, vetores[i].indices, n) for i in range(vetores.shape[0])]
    )


def separar_anime_nota_maxima(matriz, random_state):
    """Retira de cada usuário um anime nota 10 (alvo do hit rate)."""
    rng = np.random.default_rng(random_state)
    matriz = matriz.tolil(copy=True)
    alvos = np.empty(matriz.shape[0], dtype=int)
    for i, (colunas, notas) in enumerate(zip(matriz.rows, matriz.data)):
        alvos[i] = rng.choice([c for c, nota in zip(colunas, notas) if nota == 10])
        matriz[i, alvos[i]] = 0
    return matriz.tocsr(), alvos


def hit_rate(recomendacoes, alvos):
    return float((recomendacoes == alvos[:, None]).any(axis=1).mean())


def serendipity(recomendacoes, top_populares):
    """Fração das recomendações que está no top de populares (menor = mais novidade)."""
    return float(np.isin(recomendacoes, top_populares).mean())
