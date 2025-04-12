import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY  = os.getenv('SECRET_KEY')
    MONGO_URI  = os.getenv('MONGO_URI' )
    ALGORITHM  = os.getenv('ALGORITHM' )
    SESSION_COOKIE_NAME  = os.getenv('SESSION_COOKIE_NAME')
    ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    MONGO_DB_NAME : str = os.getenv('MONGO_DB_NAME',"auth_fastapi")

