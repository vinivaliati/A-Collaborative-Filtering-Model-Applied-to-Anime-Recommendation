import matplotlib.pyplot as plt

from .config import PASTA_IMAGENS

AZUL = "#2a78d6"
CINZA = "#898781"
TEXTO = "#52514e"

ROTULOS = {
    "cosine": "Cosine",
    "manhattan": "Manhattan",
    "euclidean": "Euclidean",
    "item": "Item-based",
    "top10": "Top 10 animes",
    "top3": "Top 3 animes",
}


def configurar_estilo():
    plt.rcParams.update(
        {
            "figure.facecolor": "#fcfcfb",
            "axes.facecolor": "#fcfcfb",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": CINZA,
            "axes.labelcolor": TEXTO,
            "xtick.color": CINZA,
            "ytick.color": CINZA,
            "axes.titlelocation": "left",
            "axes.titleweight": "bold",
            "figure.dpi": 110,
        }
    )


def barras_horizontais(serie, titulo, xlabel=None, formato="{:,.0f}", arquivo=None, ax=None):
    """Barras de uma cor só, ordenadas, com o valor escrito na ponta."""
    serie = serie.sort_values()
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 0.35 * len(serie) + 1.2))
    barras = ax.barh(serie.index.astype(str), serie.values, color=AZUL, height=0.6)
    ax.bar_label(barras, labels=[formato.format(v) for v in serie.values], padding=4, color=TEXTO)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)
    ax.margins(x=0.15)
    if arquivo:
        ax.figure.savefig(PASTA_IMAGENS / arquivo, bbox_inches="tight")
    return ax
