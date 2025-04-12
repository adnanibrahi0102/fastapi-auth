from passlib.context import CryptContext
from app.config import Config
from itsdangerous import URLSafeTimedSerializer

# This below line is used to create a password
# hashing context using bcrypt algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

if Config.SECRET_KEY is None:
    raise ValueError("SECRET_KEY is not set in the environment variables.")

serializer = URLSafeTimedSerializer(Config.SECRET_KEY)


def hash_password(password:str)-> str:
    """
    Hash a password using bcrypt alogorithm.
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Error hashing password: {e}")
        return ""

def verify_password(plain_password : str , hashed_password : str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    try:
        return pwd_context.verify(plain_password , hashed_password)
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def create_session_token(user_data:dict) -> str:
    """
    Create a session token for the user using the secret key.
    """
    try:
        return serializer.dumps(user_data, salt = str(10))
    except Exception as e:
        print(f"Error creating session token: {e}")
        return ""

def verify_session_token(token:str , max_age:int = 3600)-> dict:
    """
    Verify the session token and return the user data.
    """
    try:
        return serializer.loads(token, max_age=max_age)
    except Exception as e:
        print(f"Error verifying session token: {e}")
        return {}