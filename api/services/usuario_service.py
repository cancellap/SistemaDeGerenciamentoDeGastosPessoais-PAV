from sqlalchemy.exc import IntegrityError

from ..entities.usuario import Usuario
from ..repositories.usuario_repository import UsuarioRepository
from ..schemas.usuario_schema import UsuarioCreate, UsuarioUpdate


class UsuarioNaoEncontradoError(Exception):
    pass


class UsuarioEmailDuplicadoError(Exception):
    pass


class UsuarioComGastosError(Exception):
    pass


class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def create(self, data: UsuarioCreate) -> Usuario:
        nome = data.nome.strip()
        email = data.email.strip()
        if self.repository.get_by_email(email) is not None:
            raise UsuarioEmailDuplicadoError(
                "Já existe um usuário com este e-mail."
            )
        usuario = Usuario(nome=nome, email=email)
        try:
            return self.repository.create(usuario)
        except IntegrityError as error:
            raise UsuarioEmailDuplicadoError(
                "Já existe um usuário com este e-mail."
            ) from error

    def get(self, usuario_id: int) -> Usuario:
        usuario = self.repository.get(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontradoError("Usuário não encontrado.")
        return usuario

    def get_all(self) -> list[Usuario]:
        return self.repository.get_all()

    def update(self, usuario_id: int, data: UsuarioUpdate) -> Usuario:
        usuario = self.get(usuario_id)
        nome = data.nome.strip()
        email = data.email.strip()
        usuario_com_email = self.repository.get_by_email(email)
        if usuario_com_email is not None and usuario_com_email.id != usuario_id:
            raise UsuarioEmailDuplicadoError(
                "Já existe um usuário com este e-mail."
            )
        try:
            return self.repository.update(usuario, nome, email)
        except IntegrityError as error:
            raise UsuarioEmailDuplicadoError(
                "Já existe um usuário com este e-mail."
            ) from error

    def delete(self, usuario_id: int) -> None:
        usuario = self.get(usuario_id)
        if usuario.gastos:
            raise UsuarioComGastosError(
                "Não é possível excluir um usuário que possui gastos."
            )
        self.repository.delete(usuario)
