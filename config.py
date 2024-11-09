import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1234@localhost/avi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
