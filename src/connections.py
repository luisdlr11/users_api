from pymongo import MongoClient
import os

class ConnectionMongo():
    uri = ""
    connection = None
    def mongo_connect(self,uri = None):
        if uri:
            self.uri = uri
        else:
            self.uri = os.environ.get('MONGO_URI')
        try:
            self.connection =  MongoClient(self.uri,maxPoolSize=20)
            return self.connection
        except Exception as exception:
            print(exception)
            return None
        
    def mongo_close(self):
        self.connection.close()