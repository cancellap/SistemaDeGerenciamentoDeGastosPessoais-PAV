from sqlalchemy import select
from sqlalchemy.orm import Session

from ..entities.gasto import Gasto


class GastoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, gasto: Gasto) -> Gasto:
        self.db.add(gasto)
        self.db.commit()
        self.db.refresh(gasto)
        return gasto

    def get(self, gasto_id: int) -> Gasto | None:
        return self.db.get(Gasto, gasto_id)

    def get_all(self) -> list[Gasto]:
        statement = select(Gasto).order_by(Gasto.id)
        return list(self.db.scalars(statement).all())

    def update(
        self,
        gasto: Gasto,
        descricao: str,
        valor,
        data,
        usuario_id: int,
        categoria_id: int,
    ) -> Gasto:
        gasto.descricao = descricao
        gasto.valor = valor
        gasto.data = data
        gasto.usuario_id = usuario_id
        gasto.categoria_id = categoria_id
        self.db.commit()
        self.db.refresh(gasto)
        return gasto

    def delete(self, gasto: Gasto) -> None:
        self.db.delete(gasto)
        self.db.commit()
