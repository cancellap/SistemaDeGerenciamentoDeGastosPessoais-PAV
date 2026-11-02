"""Aparência visual da interface (ttk.Style)."""

from tkinter import font as tkfont
from tkinter import ttk

COR_FUNDO = "#F1F5F9"
COR_PAINEL = "#FFFFFF"
COR_TEXTO = "#0F172A"
COR_TEXTO_SUAVE = "#64748B"
COR_DESTAQUE = "#0D9488"
COR_DESTAQUE_HOVER = "#0F766E"
COR_SELECAO = "#CCFBF1"
COR_BORDA = "#E2E8F0"
COR_ABA = "#E2E8F0"
COR_PERIGO = "#DC2626"
COR_PERIGO_FUNDO = "#FEF2F2"
COR_CABECALHO = "#0F766E"
COR_CABECALHO_TEXTO = "#FFFFFF"
COR_CABECALHO_SUB = "#CCFBF1"
# Fundos suaves para listas / blocos internos (visual mais arejado).
COR_LISTA_CABECALHO = "#E6FFFA"
COR_LISTA_FUNDO = "#F7FFFD"
COR_BLOCO = "#F0FDFA"

# Preferência de fonte no estilo da referência (Inter/Poppins).
# Se não estiver instalada, cai para Segoe UI.
FAMILIA_FONTE = "Segoe UI"
# Incremento leve sobre os tamanhos de design (legibilidade).
AJUSTE_TAMANHO_FONTE = 1
# Altura de cada linha da Treeview (botões de ação usam o mesmo valor).
ALTURA_LINHA_LISTA = 40



def fonte(tamanho: int = 10, negrito: bool = False):
    """Monta a tupla de fonte usada em toda a interface."""
    peso = "bold" if negrito else "normal"
    return (FAMILIA_FONTE, tamanho + AJUSTE_TAMANHO_FONTE, peso)


def _escolher_familia_fonte() -> str:
    """Escolhe a fonte mais parecida com a referência, se existir no Windows."""
    disponiveis = {nome.lower(): nome for nome in tkfont.families()}
    for candidata in (
        "Inter",
        "Poppins",
        "Montserrat",
        "Bahnschrift",
        "Segoe UI",
    ):
        if candidata.lower() in disponiveis:
            return disponiveis[candidata.lower()]
    return "Segoe UI"


def aplicar_tema(janela) -> None:
    """Configura o tema visual da janela raiz e dos widgets ttk."""
    global FAMILIA_FONTE
    FAMILIA_FONTE = _escolher_familia_fonte()

    janela.configure(bg=COR_FUNDO)

    estilo = ttk.Style(janela)
    estilo.theme_use("clam")

    estilo.configure(
        ".", font=fonte(10), foreground=COR_TEXTO, background=COR_FUNDO
    )
    estilo.configure("TFrame", background=COR_FUNDO)
    estilo.configure("TLabel", background=COR_FUNDO, foreground=COR_TEXTO)

    estilo.configure("Cabecalho.TFrame", background=COR_CABECALHO)
    estilo.configure(
        "Cabecalho.TLabel",
        background=COR_CABECALHO,
        foreground=COR_CABECALHO_TEXTO,
        font=fonte(20, True),
    )
    estilo.configure(
        "CabecalhoSub.TLabel",
        background=COR_CABECALHO,
        foreground=COR_CABECALHO_SUB,
        font=fonte(10),
    )
    estilo.configure("Acento.TFrame", background=COR_DESTAQUE)

    estilo.configure("Card.TFrame", background=COR_PAINEL)
    estilo.configure(
        "Card.TLabel",
        background=COR_PAINEL,
        foreground=COR_TEXTO,
        font=fonte(10),
    )
    estilo.configure(
        "MetricaValor.TLabel",
        background=COR_PAINEL,
        foreground=COR_DESTAQUE,
        font=fonte(18, True),
    )
    estilo.configure(
        "Modo.TLabel",
        foreground=COR_DESTAQUE,
        background=COR_FUNDO,
        font=fonte(10, True),
    )
    estilo.configure(
        "Secao.TLabel",
        foreground=COR_TEXTO,
        background=COR_FUNDO,
        font=fonte(12, True),
    )

    estilo.configure(
        "TButton",
        background=COR_DESTAQUE,
        foreground="#FFFFFF",
        padding=(16, 9),
        font=fonte(10),
        borderwidth=0,
        focusthickness=0,
        relief="flat",
    )
    estilo.map(
        "TButton",
        background=[("active", COR_DESTAQUE_HOVER), ("pressed", "#115E59")],
    )

    estilo.configure(
        "Treeview",
        background=COR_LISTA_FUNDO,
        fieldbackground=COR_LISTA_FUNDO,
        foreground=COR_TEXTO,
        rowheight=ALTURA_LINHA_LISTA,
        font=fonte(10),

        borderwidth=0,
        relief="flat",
        highlightthickness=0,
    )
    estilo.map(
        "Treeview",
        background=[("selected", COR_SELECAO)],
        foreground=[("selected", COR_TEXTO)],
    )
    # Sem barra/linhas nativas do heading — usamos cabeçalho próprio.
    estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    estilo.configure(
        "TEntry",
        padding=9,
        fieldbackground="#F8FAFC",
        bordercolor=COR_BORDA,
        lightcolor=COR_BORDA,
        darkcolor=COR_BORDA,
        relief="flat",
        font=fonte(10),
    )
    estilo.map(
        "TEntry",
        bordercolor=[("focus", COR_DESTAQUE)],
        lightcolor=[("focus", COR_DESTAQUE)],
        darkcolor=[("focus", COR_DESTAQUE)],
        fieldbackground=[("focus", COR_PAINEL)],
    )
    estilo.configure(
        "TCombobox",
        padding=8,
        fieldbackground="#F8FAFC",
        bordercolor=COR_BORDA,
        arrowsize=14,
        relief="flat",
        font=fonte(10),
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", "#F8FAFC")],
        bordercolor=[("focus", COR_DESTAQUE)],
    )
