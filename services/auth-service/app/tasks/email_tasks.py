from app.core.logger import logger
from app.core.celery_app import celery_app
from app.services.email_service import EmailService

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
    try:
        EmailService.send_verification_email(email, verification_link)
        logger.info("Verification email sent successfully to {email")
        logger.info("=" * 50)
        return True
    except Exception as e:
        logger.exception(f"Failed to send verification email to {email}: {e}")
        logger.info("=" * 50)
        return False

    return True

@celery_app.task
def send_reset_password_email(email: str, otp: str):
    try:
        logger.info("=" * 50)
        EmailService.send_reset_password_email(email,otp)
        logger.info(f"Reset password email sent successfully to {email}")
        logger.info("=" * 50)
        return True

    except Exception as e:
        logger.exception(f"Failed to send reset password email to {email}: {e}")
        logger.info("=" * 50)
        return False

    return True