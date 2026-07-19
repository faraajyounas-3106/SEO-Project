import uuid
from sqlalchemy import Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class AuditMetrics(Base):
    __tablename__ = "audit_metrics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id", ondelete="CASCADE"), nullable=False)
    lcp: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cls: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    mobile_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    desktop_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    json_report: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    # Relationships
    audit: Mapped["Audit"] = relationship("Audit", back_populates="metrics")

    def __repr__(self) -> str:
        return f"<AuditMetrics {self.id} Audit ID: {self.audit_id}>"
