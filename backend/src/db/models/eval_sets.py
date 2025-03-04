from uuid import uuid4, UUID
from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class EvalSets(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(index=True)

    colors: Mapped[list["ColorsEval"]] = relationship(
        "ColorsEval", back_populates="eval_sets"
    )
    thousand: Mapped[list["ThousandEval"]] = relationship(
        "ThousandEval", back_populates="eval_sets"
    )
    mass_pro: Mapped[list["MassProEval"]] = relationship(
        "MassProEval", back_populates="eval_sets"
    )

    def __repr__(self):
        return f"<EvalSets(id={self.id}, item='{self.item}')>"
