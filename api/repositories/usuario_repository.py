from sqlalchemy import select
from sqlalchemy.orm import Session

from ..entities.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def get(self, usuario_id: int) -> Usuario | None:
        return self.db.get(Usuario, usuario_id)

    def get_all(self) -> list[Usuario]:
        statement = select(Usuario).order_by(Usuario.id)
        return list(self.db.scalars(statement).all())

    def get_by_email(self, email: str) -> Usuario | None:
        statement = select(Usuario).where(Usuario.email == email)
        return self.db.scalar(statement)

    def update(self, usuario: Usuario, nome: str, email: str) -> Usuario:
        usuario.nome = nome
        usuario.email = email
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> None:
        self.db.delete(usuario)
        self.db.commit()
