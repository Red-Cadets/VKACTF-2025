from datetime import timedelta
import os

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')


class Config:
    JWT_EXPIRATION_DELTA = timedelta(days=1)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@web-m-hawk-postgres:5432/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
