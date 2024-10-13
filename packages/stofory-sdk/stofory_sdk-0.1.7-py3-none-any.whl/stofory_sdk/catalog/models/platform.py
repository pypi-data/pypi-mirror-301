from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any


from advanced_alchemy.base import BigIntAuditBase, SlugKey
from sqlalchemy.dialects.postgresql import VARCHAR, TEXT, JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .decorator.jsonb_dict import JSONBDict

if TYPE_CHECKING:
    from .product_platform import ProductPlatform


class Platform(BigIntAuditBase, SlugKey):
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[str] = mapped_column(TEXT(), nullable=False)
    custom_fields_template: Mapped[Dict[str, Any]] = mapped_column(JSONBDict, default={})

    product_platforms: Mapped[list[ProductPlatform]] = relationship(
        back_populates="platform",
        lazy="selectin",
        uselist=True,
        cascade="all, delete"
    )
