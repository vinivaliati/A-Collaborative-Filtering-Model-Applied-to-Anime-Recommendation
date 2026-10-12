# Modelo de filtragem colaborativa aplicada à recomendação de animes

*A Collaborative Filtering Model Applied to Anime Recommendation*

🇺🇸 [Read in English](README.md)

Reconstrução do meu TCC da Especialização em Data Science & Big Data (UFPR, 2024).
O texto original está em [`referencias/monografia.pdf`](referencias/monografia.pdf).

![Demonstração do app](relatorios/imagens/app.gif)

## O problema

Recomendar animes para um usuário **novo**, sem nenhum histórico de avaliações (*cold start*).

## A solução

1. **Clusterização (K-means):** os animes são agrupados em 20 clusters pelas suas características. O anime mais popular de cada cluster vira uma "persona".
2. **Filtragem colaborativa baseada em usuários:** o usuário escolhe até 3 personas, o modelo busca os usuários mais parecidos (`NearestNeighbors`, força bruta) e recomenda o que eles mais gostaram. Três distâncias são comparadas: Cosseno, Manhattan e Euclidiana.

## Resultados

| Modelo | Hit Rate ↑ | Serendipity ↓ | Animes diferentes recomendados ↑ |
|---|---|---|---|
| **Cosine** | **38,0%** | **42,2%** | 104 |
| Manhattan | 35,8% | 48,3% | 37 |
| Euclidean | 35,8% | 54,7% | 29 |
| Item-based (baseline) | 25,6% | 49,4% | 110 |
| Top 10 animes (baseline) | 18,3% | — | — |
| Top 3 animes (baseline) | 8,7% | — | — |

- **Hit Rate:** esconde-se um anime nota 10 de cada usuário de teste; é *hit* se ele aparece nas 10 recomendações.
- **Serendipity:** fração das recomendações que cai no Top 10 de animes mais populares, em todas as combinações de até 3 personas. Menor = mais novidade.

A filtragem colaborativa acerta cerca de duas vezes mais do que recomendar os animes mais populares.
Nesta reprodução a distância Cosseno foi a melhor nas duas métricas. Na monografia a escolhida foi a Manhattan, pela menor Serendipity; essa diferença está discutida em [`04_avaliacao.ipynb`](notebooks/04_avaliacao.ipynb).

![Hit Rate](relatorios/imagens/hit_rate.png)

## Organização

```
├── dados                <- dados originais (não versionados) e tratados
├── modelos              <- K-means e matriz usuário × anime
├── notebooks
│   ├── 01_eda.ipynb                      <- exploração e tratamento
│   ├── 02_clusterizacao.ipynb            <- Modelo 1: K-means e personas
│   ├── 03_filtragem_colaborativa.ipynb   <- Modelo 2: recomendação
│   ├── 04_avaliacao.ipynb                <- Hit Rate e Serendipity
│   └── src              <- config, funções auxiliares, gráficos e modelos
├── referencias          <- monografia, sobre a base e dicionário de dados
├── relatorios/imagens   <- gráficos gerados pelos notebooks
├── home.py              <- app Streamlit
└── requirements.txt
```

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

streamlit run home.py
```

O app funciona direto, porque os dados tratados e os modelos estão versionados.

Para refazer tudo do zero, baixe a [base do Kaggle](https://www.kaggle.com/datasets/hernan4444/anime-recommendation-database-2020), coloque `anime.csv`, `anime_with_synopsis.csv` e `rating_complete.csv` em `dados/` e rode os notebooks na ordem.
