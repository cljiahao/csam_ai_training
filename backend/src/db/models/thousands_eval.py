from datetime import datetime as dt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from db.base import Base


class ThousandsEval(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    small: Mapped[int] = mapped_column(default=0)
    medium: Mapped[int] = mapped_column(default=0)
    big: Mapped[int] = mapped_column(default=0)

    # Relationship to EvalSet
    eval_sets: Mapped["EvalSets"] = relationship("EvalSets", back_populates="thousands")

    # Foreign key to ChipLotDetails
    eval_sets_id: Mapped[UUID] = mapped_column(ForeignKey("evalsets.id"))

    def __repr__(self):
        return f"<ThousandsEval(id={self.id}, eval_sets_id='{self.eval_sets_id}')>"
