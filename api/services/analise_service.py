from decimal import Decimal, ROUND_HALF_UP

from ..entities.gasto import Gasto
from ..repositories.gasto_repository import GastoRepository


class AnaliseService:
    def __init__(self, repository: GastoRepository):
        self.repository = repository

    def get_total(self) -> dict[str, float]:
        gastos = self.repository.get_all()
        total = Decimal("0")
        for gasto in gastos:
            total += gasto.valor
        return {"total": self._to_float(total)}

    def get_media(self) -> dict[str, float]:
        gastos = self.repository.get_all()
        media = self._calcular_media(gastos)
        return {"media": self._to_float(media)}

    def get_por_categoria(self) -> list[dict[str, str | float]]:
        gastos = self.repository.get_all()
        totais: dict[str, Decimal] = {}
        for gasto in gastos:
            nome = gasto.categoria.nome
            totais[nome] = totais.get(nome, Decimal("0")) + gasto.valor

        categorias = [
            {"categoria": nome, "total": self._to_float(total)}
            for nome, total in totais.items()
        ]
        return sorted(categorias, key=lambda item: item["total"], reverse=True)

    def get_anomalias(self) -> list[dict[str, str | float]]:
        gastos = self.repository.get_all()
        media = self._calcular_media(gastos)
        limite = media * Decimal("2")
        anomalias = []

        for gasto in gastos:
            if gasto.valor > limite:
                anomalias.append(
                    {
                        "descricao": gasto.descricao,
                        "valor": self._to_float(gasto.valor),
                        "media": self._to_float(media),
                    }
                )
        return anomalias

    def _calcular_media(self, gastos: list[Gasto]) -> Decimal:
        if not gastos:
            return Decimal("0")

        total = Decimal("0")
        for gasto in gastos:
            total += gasto.valor
        return total / Decimal(len(gastos))

    def _to_float(self, valor: Decimal) -> float:
        arredondado = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return float(arredondado)
