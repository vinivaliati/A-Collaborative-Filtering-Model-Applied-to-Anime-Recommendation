from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

PASTA_DADOS = PASTA_PROJETO / "dados"

# dados originais (Kaggle: hernan4444/anime-recommendation-database-2020)
DADOS_ANIMES = PASTA_DADOS / "anime.csv"
DADOS_SINOPSES = PASTA_DADOS / "anime_with_synopsis.csv"
DADOS_AVALIACOES = PASTA_DADOS / "rating_complete.csv"

# dados tratados
ANIMES_TRATADOS = PASTA_DADOS / "animes_tratados.parquet"
ANIMES_FEATURES = PASTA_DADOS / "animes_features.parquet"
ANIMES_CLUSTERS = PASTA_DADOS / "animes_clusters.parquet"

PASTA_MODELOS = PASTA_PROJETO / "modelos"
MODELO_KMEANS = PASTA_MODELOS / "kmeans.joblib"
MATRIZ_USUARIO_ANIME = PASTA_MODELOS / "matriz_usuario_anime.joblib"

PASTA_RELATORIOS = PASTA_PROJETO / "relatorios"
PASTA_IMAGENS = PASTA_RELATORIOS / "imagens"
PASTA_CAPAS = PASTA_IMAGENS / "capas"
METRICAS = PASTA_RELATORIOS / "metricas.csv"

RANDOM_STATE = 42

# amostragem das avaliações
MIN_AVALIACOES_USUARIO = 50
N_USUARIOS = 20_000
MIN_AVALIACOES_ANIME = 50

# modelos
N_CLUSTERS = 20
N_ESTUDIOS = 20
K_VIZINHOS = 50
N_RECOMENDACOES = 10
MAX_PERSONAS = 3
METRICAS_DISTANCIA = ["cosine", "manhattan", "euclidean"]
