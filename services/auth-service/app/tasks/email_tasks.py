from app.core.logger import logger
from app.core.celery_app import celery_app

#registers the function as a Celery task
@celery_app.task
def send_welcome_email(email:str):
    logger.info("=" * 50)
    logger.info(f"Sending welcome email to {email}")
    logger.info("Welcome email sent successfully")
    logger.info("=" * 50)
    return True

@celery_app.task
def send_verification_email(email: str, verification_link: str):
    logger.info("=" * 50)
    logger.info(f"Sending verification email to {email}")
    logger.info(f"Verification Link: {verification_link}")
    logger.info("Verification email sent successfully")
    logger.info("=" * 50)

    return True

@celery_app.task
def send_reset_password_email(email: str, otp:str):
    logger.info("=" * 50)
    logger.info(f"Sending password reset OTP to {email}")
    logger.info(f"OTP: {otp}")
    logger.info("=" * 50)

    return True