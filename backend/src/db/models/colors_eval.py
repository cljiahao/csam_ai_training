from datetime import datetime as dt
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from db.base import Base


class ColorsEval(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    black_big: Mapped[int] = mapped_column(default=0)
    blue_small: Mapped[int] = mapped_column(default=0)
    blue_medium: Mapped[int] = mapped_column(default=0)
    blue_big: Mapped[int] = mapped_column(default=0)
    cyan_small: Mapped[int] = mapped_column(default=0)
    cyan_medium: Mapped[int] = mapped_column(default=0)
    cyan_big: Mapped[int] = mapped_column(default=0)
    green_small: Mapped[int] = mapped_column(default=0)
    green_medium: Mapped[int] = mapped_column(default=0)
    green_big: Mapped[int] = mapped_column(default=0)
    lime_small: Mapped[int] = mapped_column(default=0)
    lime_medium: Mapped[int] = mapped_column(default=0)
    lime_big: Mapped[int] = mapped_column(default=0)
    orange_small: Mapped[int] = mapped_column(default=0)
    orange_medium: Mapped[int] = mapped_column(default=0)
    orange_big: Mapped[int] = mapped_column(default=0)
    yellow_small: Mapped[int] = mapped_column(default=0)
    yellow_medium: Mapped[int] = mapped_column(default=0)
    yellow_big: Mapped[int] = mapped_column(default=0)

    # Relationship to EvalSet
    eval_sets: Mapped["EvalSets"] = relationship("EvalSets", back_populates="colors")

    # Foreign key to ChipLotDetails
    eval_sets_id: Mapped[UUID] = mapped_column(ForeignKey("evalsets.id"))

    def __repr__(self):
        return f"<ColorEval(id={self.id}, eval_sets_id='{self.eval_sets_id}')>"
