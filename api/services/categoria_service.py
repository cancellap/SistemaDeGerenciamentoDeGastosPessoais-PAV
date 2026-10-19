from ..entities.categoria import Categoria
from ..repositories.categoria_repository import CategoriaRepository
from ..schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


class CategoriaNaoEncontradaError(Exception):
    pass


class CategoriaComGastosError(Exception):
    pass


class CategoriaService:
    def __init__(self, repository: CategoriaRepository):
        self.repository = repository

    def create(self, data: CategoriaCreate) -> Categoria:
        categoria = Categoria(nome=data.nome.strip())
        return self.repository.create(categoria)

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
        return self.repository.update(categoria, data.nome.strip())

    def delete(self, categoria_id: int) -> None:
        categoria = self.get(categoria_id)
        if categoria.gastos:
            raise CategoriaComGastosError(
                "Não é possível excluir uma categoria que possui gastos."
            )
        self.repository.delete(categoria)
