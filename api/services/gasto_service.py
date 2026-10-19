from ..entities.gasto import Gasto
from ..repositories.categoria_repository import CategoriaRepository
from ..repositories.gasto_repository import GastoRepository
from ..repositories.usuario_repository import UsuarioRepository
from ..schemas.gasto_schema import GastoCreate, GastoUpdate


class GastoNaoEncontradoError(Exception):
    pass


class ValorGastoInvalidoError(Exception):
    pass


class CategoriaGastoNaoEncontradaError(Exception):
    pass


class UsuarioGastoNaoEncontradoError(Exception):
    pass


class GastoService:
    def __init__(
        self,
        repository: GastoRepository,
        usuario_repository: UsuarioRepository,
        categoria_repository: CategoriaRepository,
    ):
        self.repository = repository
        self.usuario_repository = usuario_repository
        self.categoria_repository = categoria_repository

    def create(self, data: GastoCreate) -> Gasto:
        self._validate_data(data)
        gasto = Gasto(
            descricao=data.descricao.strip(),
            valor=data.valor,
            data=data.data,
            usuario_id=data.usuario_id,
            categoria_id=data.categoria_id,
        )
        return self.repository.create(gasto)

    def get(self, gasto_id: int) -> Gasto:
        gasto = self.repository.get(gasto_id)
        if gasto is None:
            raise GastoNaoEncontradoError("Gasto não encontrado.")
        return gasto

    def get_all(self) -> list[Gasto]:
        return self.repository.get_all()

    def update(self, gasto_id: int, data: GastoUpdate) -> Gasto:
        gasto = self.get(gasto_id)
        self._validate_data(data)
        return self.repository.update(
            gasto,
            data.descricao.strip(),
            data.valor,
            data.data,
            data.usuario_id,
            data.categoria_id,
        )

    def delete(self, gasto_id: int) -> None:
        gasto = self.get(gasto_id)
        self.repository.delete(gasto)

    def _validate_data(self, data: GastoCreate | GastoUpdate) -> None:
        if data.valor <= 0:
            raise ValorGastoInvalidoError(
                "O valor do gasto deve ser maior que zero."
            )
        if self.usuario_repository.get(data.usuario_id) is None:
            raise UsuarioGastoNaoEncontradoError("Usuário não encontrado.")
        if self.categoria_repository.get(data.categoria_id) is None:
            raise CategoriaGastoNaoEncontradaError(
                "A categoria informada não existe."
            )
