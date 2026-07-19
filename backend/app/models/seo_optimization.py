import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class SEOOptimization(Base):
    __tablename__ = "seo_optimizations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id", ondelete="CASCADE"), nullable=False)
    url_path: Mapped[str] = mapped_column(String(255), nullable=False)
    original_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    optimized_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    original_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    optimized_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    json_ld_schema: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ai_status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    audit: Mapped["Audit"] = relationship("Audit")

    def __repr__(self) -> str:
        return f"<SEOOptimization {self.id} Status: {self.ai_status} URL: {self.url_path}>"
