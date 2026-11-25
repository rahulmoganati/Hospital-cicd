import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://medix_user:password@localhost:3306/medix_hospital?charset=utf8mb4")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
