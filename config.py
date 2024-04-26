import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    MONGODB_SETTINGS = {
        'db': 'your-db-name',
        'host': 'localhost',
        'port': 27017
    }