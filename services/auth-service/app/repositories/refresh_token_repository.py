from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository:
    @staticmethod
    def get_by_user_id(db: Session, user_id):
        return db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()

    @staticmethod
    def create(db: Session, refresh_token: RefreshToken):
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token

    @staticmethod
    def delete(db: Session, refresh_token: RefreshToken):
        db.delete(refresh_token)
        db.commit()

    @staticmethod
    def delete_by_id(db: Session, user_id):
        token = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).first()
        if token:
            db.delete(token)
            db.commit()

    @staticmethod
    def get_by_token_hash(db: Session, token_hash: str):
        return db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
        
