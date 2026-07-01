from passlib.context import CryptContext  #Passlib library for handling password hashing securely
import hashlib

# Create a hashing context using bcrypt algorithm
# "deprecated=auto" means older/weaker schemes are automatically marked as deprecated
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_password(password: str):
    # Takes a plain text password and returns a bcrypt hashed version
    # e.g. "mypassword123" → "$2b$12$eW5bJ..." (irreversible hash)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    # Compares a plain text password against a stored hash
    # Returns True if they match, False otherwise
    # e.g. used during login to check if entered password is correct
    return pwd_context.verify(plain_password, hashed_password)

def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()