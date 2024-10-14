from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase, SlugKey
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, relationship, mapped_column, declared_attr
from sqlalchemy_utils import LtreeType

if TYPE_CHECKING:
    from .product_platform_category import ProductPlatformCategory


class Category(BigIntAuditBase, SlugKey):
    @declared_attr.directive
    @classmethod
    def __table_args__(cls):
        return (
            Index("idx_category_name", "name"),
            Index("idx_category_platform_id", "platform_id"),
            Index("idx_gist_path", "path", postgresql_using='gist'),
            UniqueConstraint(
                cls.slug,
                name=f"uq_{cls.__tablename__}_slug",
            ).ddl_if(callable_=cls._create_unique_slug_constraint),
            Index(
                f"ix_{cls.__tablename__}_slug_unique",
                cls.slug,
                unique=True,
            ).ddl_if(callable_=cls._create_unique_slug_index),
        )

    platform_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("platform.id"), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(BIGINT, ForeignKey("category.id"), nullable=True)
    path: Mapped[str] = mapped_column(LtreeType(), nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    product_platform_info_categories: Mapped[list[ProductPlatformCategory]] = relationship(
        back_populates="category",
        lazy="selectin",
        uselist=False,
        cascade="all, delete"
    )
