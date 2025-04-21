from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4, UUID

from db.base import Base


class BaseSets(Base):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    date_created: Mapped[dt] = mapped_column(default=func.now())
    date_updated: Mapped[dt] = mapped_column(default=func.now(), onupdate=func.now())
    item: Mapped[str] = mapped_column(index=True)
    no_of_g: Mapped[int] = mapped_column(default=0)
    no_of_ng: Mapped[int] = mapped_column(default=0)
    no_of_others: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<BaseSets(id={self.id}, item='{self.item}')>"
