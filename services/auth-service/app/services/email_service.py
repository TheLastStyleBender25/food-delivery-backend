import resend
from app.core.config import settings

resend.api_key = settings.RESEND_API_KEY


class EmailService:
    @staticmethod
    def send_verification_email(email : str, verification_link : str):
        resend.Emails.send({
            "from": settings.EMAIL_FROM,
            "to": [email],
            "subject": "Verify your Frostbite account",
            "html": f"""
                <h2>Welcome to Frostbite</h2>

                <p>Please verify your email address.</p>

                <a href="{verification_link}">
                    Verify Email
                </a>
            """
        })


    @staticmethod
    def send_reset_password_email(email: str, otp: str):
        resend.Emails.send({
            "from": settings.EMAIL_FROM,
            "to": [email],
            "subject": "Password Reset OTP",
            "html": f"""
                <h2>Password Reset Request</h2>

                <p>Your OTP is:</p>

                <h1>{otp}</h1>

                <p>This OTP expires in 5 minutes.</p>
            """
        })