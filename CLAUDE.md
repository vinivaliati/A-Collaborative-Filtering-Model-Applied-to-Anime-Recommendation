# CLAUDE.md

Reconstrução do TCC "Modelo de filtragem colaborativa aplicada a recomendação de animes" (UFPR, 2024).
A monografia em `referencias/monografia.pdf` é a especificação do método: mudanças no modelo devem partir dela.

## Comandos

```bash
source .venv/bin/activate
streamlit run home.py                                    # app
cd notebooks && jupyter nbconvert --to notebook --execute --inplace 01_eda.ipynb   # reexecutar um notebook
```

Os notebooks rodam com `notebooks/` como diretório de trabalho (importam `from src...`).
O `home.py` roda da raiz (importa `from notebooks.src...`).

## Pipeline

Cada notebook lê o que o anterior salvou. Mudou algo em um, rode os seguintes na ordem.

1. `01_eda.ipynb`: lê os CSVs do Kaggle, amostra usuários, gera `animes_tratados.parquet`, `animes_features.parquet` e `matriz_usuario_anime.joblib`. Único que precisa dos CSVs originais (~20 s).
2. `02_clusterizacao.ipynb`: K-means (k=20), PCA e personas, gera `animes_clusters.parquet` e `kmeans.joblib`, e baixa do MyAnimeList as capas das personas que faltam em `relatorios/imagens/capas/` (precisa de internet se as personas mudarem).
3. `03_filtragem_colaborativa.ipynb`: demonstração da recomendação, não salva nada.
4. `04_avaliacao.ipynb`: Hit Rate e Serendipity, gera `relatorios/metricas.csv` e os gráficos.

## Convenções

- Código, nomes de variáveis, funções e textos em **português**, como no restante dos projetos do autor.
- Análise em **notebooks** (didáticos, com markdown explicando cada passo). Em `notebooks/src` só o que é reutilizado: `config.py` (caminhos e parâmetros), `auxiliares.py` (tratamento), `models.py` (recomendação e métricas), `graficos.py`.
- Todo caminho e parâmetro (k, tamanho da amostra, nº de vizinhos) vem de `src/config.py`. Não escrever caminho fixo em notebook.
- Direto ao ponto: sem abstrações, classes ou dependências que o projeto não precise.
- Gráficos: `barras_horizontais` de `src/graficos.py`, uma cor só, valor escrito na barra.

## Pontos que não são óbvios

- **A coluna `j` da matriz usuário × anime é a linha `j` de `animes_tratados`/`animes_clusters`.** Os modelos trabalham com esses índices posicionais, não com `MAL_ID`. Se reordenar ou filtrar os animes, a matriz precisa ser regerada pelo notebook 01.
- O app espera um arquivo `relatorios/imagens/capas/<MAL_ID>.jpg` para cada persona. Se as personas mudarem, rode o notebook 02 para baixar as novas.
- Zero na matriz significa "não avaliou" (as notas vão de 1 a 10).
- `dados/*.csv` não vai para o git (2,8 GB). Os parquets e os `.joblib` vão, para o app funcionar após o clone.
- Os textos de conclusão dos notebooks e dos READMEs citam números. Se os resultados mudarem, atualize os textos.
- O `README.md` é em inglês e o `README.pt-br.md` em português. Mudou um, mude o outro.
- A conclusão desta reprodução (Cosseno melhor nas duas métricas) difere da monografia (Manhattan escolhida). Isso é um resultado, não um bug: não ajustar o modelo para "bater" com o texto original.
