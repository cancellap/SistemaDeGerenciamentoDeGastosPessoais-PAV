from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..entities.categoria import Categoria


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, categoria: Categoria) -> Categoria:
        try:
            self.db.add(categoria)
            self.db.commit()
            self.db.refresh(categoria)
        except IntegrityError:
            self.db.rollback()
            raise
        return categoria

    def get(self, categoria_id: int) -> Categoria | None:
        return self.db.get(Categoria, categoria_id)

    def get_all(self) -> list[Categoria]:
        statement = select(Categoria).order_by(Categoria.id)
        return list(self.db.scalars(statement).all())

    def get_by_name(self, nome: str) -> Categoria | None:
        statement = select(Categoria).where(Categoria.nome == nome)
        return self.db.scalar(statement)

    def update(self, categoria: Categoria, nome: str) -> Categoria:
        categoria.nome = nome
        try:
            self.db.commit()
            self.db.refresh(categoria)
        except IntegrityError:
            self.db.rollback()
            raise
        return categoria

    def delete(self, categoria: Categoria) -> None:
        self.db.delete(categoria)
        self.db.commit()
