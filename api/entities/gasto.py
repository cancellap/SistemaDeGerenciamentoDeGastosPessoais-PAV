from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.database import Base


class Gasto(Base):
    __tablename__ = "gastos"

    __table_args__ = (
        CheckConstraint("valor > 0", name="ck_gastos_valor_positivo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="gastos")
    categoria: Mapped["Categoria"] = relationship(back_populates="gastos")