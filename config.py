import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'MONGO_URI': os.getenv('MONGO_URI'),
        'DB_NAME': os.getenv('DB_NAME')
    }

