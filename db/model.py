"""BaseModel that will be used in other models."""
from datetime import datetime, timezone

import sqlalchemy as db
from .service import Base, Db


class BaseModel(Base):
    """Template for our models."""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def before_save(self, *args, **kwargs):
        """Run before save."""
        pass

    def after_save(self, *args, **kwargs):
        """Run after save."""
        pass

    def save(self, commit=True):
        """Save current obj in db."""
        self.before_save()
        Db.session.add(self)
        if commit:
            try:
                Db.session.commit()
            except Exception as err:
                Db.session.rollback()
                raise err

        self.after_save()

    def before_update(self, *args, **kwargs):
        """Before updating current obj in db."""
        pass

    def after_update(self, *args, **kwargs):
        """After updating current obj in db."""
        pass

    def update(self, *args, **kwargs):
        """Update current obj in db."""
        self.before_update(*args, **kwargs)
        Db.session.commit()
        self.after_update(*args, **kwargs)

    def delete(self, commit=True):
        """Delete current obj in db."""
        Db.session.delete(self)
        if commit:
            Db.session.commit()
