# Sobre a base

**Fonte:** [Anime Recommendation Database 2020](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020) (Kaggle, Hernan Valdivieso), coletada do [MyAnimeList](https://myanimelist.net).

Na monografia original os dados vieram direto da API do MyAnimeList. Esta versão usa a base do Kaggle, que tem as mesmas variáveis.

## Arquivos usados

Baixe o zip do Kaggle e coloque em `dados/`:

| Arquivo | Linhas | Uso |
|---|---|---|
| `anime.csv` | 17.562 animes | características dos animes (clusterização) |
| `anime_with_synopsis.csv` | 16.214 animes | sinopse exibida no app |
| `rating_complete.csv` | 57,6 milhões de notas, 310 mil usuários | filtragem colaborativa |

`animelist.csv` e `watching_status.csv` também vêm no zip, mas não são usados.

## Recorte feito no projeto

Definido em `notebooks/01_eda.ipynb`, com os parâmetros em `notebooks/src/config.py`:

- animes `Rx - Hentai` removidos;
- usuários com pelo menos 50 avaliações, amostra aleatória de 20.000;
- animes com pelo menos 50 avaliações dentro da amostra.

Resultado: 20.000 usuários, 6.166 animes e 4,87 milhões de avaliações.
