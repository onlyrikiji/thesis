import os
from dotenv import load_dotenv 

class Config:
    load_dotenv('.env')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
