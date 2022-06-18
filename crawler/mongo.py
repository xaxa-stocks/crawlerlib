'''Class to connect to mongo db'''
import os
from pymongo import MongoClient
import certifi

class MongoConnect():
    '''Class to connect to mongodb'''

    username = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    def __init__(self):
        pass

    def connect(self,col_name: str):
        """
        Method to connect to a predefined mongodb atlas cluster.

        Args: col_name >>> Collection name to connect to
        """
        client = MongoClient(f'mongodb+srv://{self.username}:{self.password}@fii-api.gnuy4.mongodb.net/{self.db_name}?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        db_conn = client[self.db_name][col_name]
        return db_conn
        
    # def __enter__(self, *exec):
    #     return self

    # def __exit__(self, *exec):
    #     if self.client:
    #         self.client.close()