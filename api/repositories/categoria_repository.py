from sqlalchemy import select
from sqlalchemy.orm import Session

from ..entities.categoria import Categoria


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, categoria: Categoria) -> Categoria:
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def get(self, categoria_id: int) -> Categoria | None:
        return self.db.get(Categoria, categoria_id)

    def get_all(self) -> list[Categoria]:
        statement = select(Categoria).order_by(Categoria.id)
        return list(self.db.scalars(statement).all())

    def update(self, categoria: Categoria, nome: str) -> Categoria:
        categoria.nome = nome
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, categoria: Categoria) -> None:
        self.db.delete(categoria)
        self.db.commit()
