import mysql.connector
import os

from dotenv import load_dotenv
from modules.ErrorHandling import logger

class Database:
    def __init__(self):
        load_dotenv()
        self.connect = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USERNAME'),
            passwd=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            autocommit=True
        )
        self.cursor = self.connect.cursor(buffered=True)
        logger.info("Database Connected Successfully")
    
db = Database()
