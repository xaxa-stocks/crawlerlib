'''Class to connect to mongo db'''
import os
from pymongo import MongoClient
import certifi

class MongoConnect():
    '''Class to connect to mongodb'''

    def __init__(self):
        self.username = os.environ['DB_USERNAME']
        self.password = os.environ['DB_PASSWORD']
        self.db_name = os.environ['DB_NAME']

    def return_connection_string(self):
        """returns a connection string"""
        db_string = f'mongodb+srv://{self.username}:{self.password}'
        db_string += f'@fii-api.gnuy4.mongodb.net/{self.db_name}'
        db_string += '?retryWrites=true&w=majority'
        return db_string

    def connect(self,col_name: str):
        """
        Method to connect to a predefined mongodb atlas cluster.

        Args: col_name >>> Collection name to connect to
        """
        client = MongoClient(self.return_connection_string(), tlsCAFile=certifi.where())
        return client[self.db_name][col_name]
        