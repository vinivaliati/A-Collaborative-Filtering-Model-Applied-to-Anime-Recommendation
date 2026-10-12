# Dicionário de dados

## `anime.csv`

| Coluna | Descrição | Usada no modelo? |
|---|---|---|
| `MAL_ID` | ID do anime no MyAnimeList | chave |
| `Name` | Nome | exibição |
| `Score` | Nota média (1 a 10) | não (viés de popularidade) |
| `Genres` | Gêneros, separados por vírgula | sim, *dummies* |
| `English name`, `Japanese name` | Nomes alternativos | não |
| `Type` | TV, Movie, OVA, ONA, Special, Music | sim, *dummies* |
| `Episodes` | Número de episódios | sim, em faixas (`Tamanho`) |
| `Aired` | Período de exibição | sim, ano em faixas (`Faixa de ano`) |
| `Premiered` | Temporada de estreia | não (73% ausente) |
| `Producers`, `Licensors` | Produtores e licenciadores | não |
| `Studios` | Estúdios | sim, *dummies* dos 20 mais frequentes |
| `Source` | Origem (Manga, Original, Light novel...) | sim, *dummies* |
| `Duration` | Duração por episódio | não |
| `Rating` | Classificação etária | sim, *dummies* |
| `Ranked` | Posição no ranking de nota | não (viés de popularidade) |
| `Popularity` | Posição no ranking de popularidade (1 = mais popular) | sim, única variável de popularidade |
| `Members`, `Favorites`, `Watching`, `Completed`, `On-Hold`, `Dropped`, `Plan to Watch` | Contagens de usuários por situação | não (viés de popularidade) |
| `Score-10` ... `Score-1` | Quantidade de usuários que deu cada nota | não (viés de popularidade) |

Valores ausentes aparecem como o texto `Unknown`.

## `rating_complete.csv`

Só contém animes que o usuário **terminou** e **avaliou**.

| Coluna | Descrição |
|---|---|
| `user_id` | ID anônimo do usuário |
| `anime_id` | `MAL_ID` do anime |
| `rating` | Nota de 1 a 10 |

## Arquivos gerados

| Arquivo | Conteúdo |
|---|---|
| `dados/animes_tratados.parquet` | animes do recorte, com `Ano`, `Faixa de ano`, `Tamanho`, `Sinopse` |
| `dados/animes_features.parquet` | 96 variáveis do K-means, uma linha por anime |
| `dados/animes_clusters.parquet` | `animes_tratados` + `Cluster`, `PCA 1`, `PCA 2`, `Persona`, `Descrição do cluster` |
| `modelos/kmeans.joblib` | pipeline `MinMaxScaler` + `KMeans` |
| `modelos/matriz_usuario_anime.joblib` | matriz esparsa de notas, usuários × animes (colunas na ordem de `animes_tratados`) |
| `relatorios/metricas.csv` | Hit Rate, Serendipity e diversidade por modelo |
