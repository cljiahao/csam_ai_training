from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class ReTrainSets(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(unique=True, index=True)
    no_of_g: Mapped[int] = mapped_column(default=0)
    no_of_ng: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<ReTrainSets(id={self.id}, item='{self.item}')>"
