from sqlalchemy.orm import Session   # Session class — represents an active connection/transaction with the DB
from app.models.user import User     # SQLAlchemy User model (maps to the "users" table)

class UserRepository:
    """Manages persistence operations for ORM-mapped models."""
    # Repository pattern — centralizes all DB operations for User in one place
    # @staticmethod means no need to instantiate the class, call directly as UserRepository.get_by_email(...)

    @staticmethod
    def get_by_email(db: Session, email: str):
        # Queries the DB for a user with a matching email
        # .filter() → WHERE email = <email>
        # .first()  → returns the first match or None if not found
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user: User):
        db.add(user)        # Stages the new User object to be inserted (not saved yet)
        db.commit()         # Commits the transaction — actually writes to the DB
        db.refresh(user)    # Refreshes the object with DB-generated values (e.g. id, created_at)
        return user         # Returns the fully populated user object

    @staticmethod
    def get_by_id(db: Session, user_id):
        # Queries the DB for a user with a matching ID
        # Returns the User object or None if no match found
        return db.query(User).filter(User.id == user_id).first()