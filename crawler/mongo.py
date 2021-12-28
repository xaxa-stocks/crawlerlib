import os
from pymongo import MongoClient
import certifi

class MongoConnect():

    '''Class to abstract connection to mongodb'''

    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    def __init__(self):
        """
        Initialization method
        """
        pass

    def connect(self,col_name):
        """
        Method to connect to a predefined mongodb atlas cluster. No arguments needed
        """
        client = MongoClient(f'mongodb+srv://{self.username}:{self.password}@fii-api.gnuy4.mongodb.net/{self.db_name}?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        db_conn = client[self.db_name][col_name]
        return db_conn