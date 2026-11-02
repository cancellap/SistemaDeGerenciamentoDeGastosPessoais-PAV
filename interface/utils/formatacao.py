"""Conversões entre o formato da tela (BR) e o formato da API."""

from datetime import datetime


def data_para_api(texto: str) -> str:
    """Converte DD/MM/AAAA para YYYY-MM-DD (ISO da API)."""
    data = datetime.strptime(texto.strip(), "%d/%m/%Y")
    return data.strftime("%Y-%m-%d")


def data_para_exibicao(texto: str) -> str:
    """Converte YYYY-MM-DD (API) para DD/MM/AAAA (formulário)."""
    data = datetime.strptime(str(texto).strip(), "%Y-%m-%d")
    return data.strftime("%d/%m/%Y")


def valor_para_api(texto: str) -> float:
    """
    Converte texto brasileiro (vírgula) para float.
    Aceita '10,50', '1.234,56' ou '10.50'.
    """
    limpo = texto.strip()
    if "," in limpo and "." in limpo:
        # Ex.: 1.234,56 -> remove milhar e troca a vírgula decimal.
        limpo = limpo.replace(".", "").replace(",", ".")
    elif "," in limpo:
        limpo = limpo.replace(",", ".")
    return float(limpo)


def valor_para_exibicao(valor) -> str:
    """Mostra o valor com vírgula, como o usuário digita."""
    numero = float(valor)
    return f"{numero:.2f}".replace(".", ",")
