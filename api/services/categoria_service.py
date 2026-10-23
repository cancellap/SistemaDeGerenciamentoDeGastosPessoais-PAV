from sqlalchemy.exc import IntegrityError

from ..entities.categoria import Categoria
from ..repositories.categoria_repository import CategoriaRepository
from ..schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


class CategoriaNaoEncontradaError(Exception):
    pass


class CategoriaComGastosError(Exception):
    pass


class CategoriaNomeDuplicadoError(Exception):
    pass


class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def create(self, data: CategoriaCreate) -> Categoria:
        nome = data.nome.strip()
        if self.repository.get_by_name(nome) is not None:
            raise CategoriaNomeDuplicadoError(
                "Já existe uma categoria com este nome."
            )
        categoria = Categoria(nome=nome)
        try:
            return self.repository.create(categoria)
        except IntegrityError as error:
            raise CategoriaNomeDuplicadoError(
                "Já existe uma categoria com este nome."
            ) from error

    def get(self, categoria_id: int) -> Categoria:
        categoria = self.repository.get(categoria_id)
        if categoria is None:
            raise CategoriaNaoEncontradaError(
                "Categoria não encontrada."
            )
        return categoria

    def get_all(self) -> list[Categoria]:
        return self.repository.get_all()

    def update(self, categoria_id: int, data: CategoriaUpdate) -> Categoria:
        categoria = self.get(categoria_id)
        nome = data.nome.strip()
        categoria_com_nome = self.repository.get_by_name(nome)
        if categoria_com_nome is not None and categoria_com_nome.id != categoria_id:
            raise CategoriaNomeDuplicadoError(
                "Já existe uma categoria com este nome."
            )
        try:
            return self.repository.update(categoria, nome)
        except IntegrityError as error:
            raise CategoriaNomeDuplicadoError(
                "Já existe uma categoria com este nome."
            ) from error

    def delete(self, categoria_id: int) -> None:
        categoria = self.get(categoria_id)
        if categoria.gastos:
            raise CategoriaComGastosError(
                "Não é possível excluir uma categoria que possui gastos."
            )
        self.repository.delete(categoria)
