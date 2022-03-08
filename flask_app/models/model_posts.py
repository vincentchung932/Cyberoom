from flask_app.config.mysqlconnection import connectToMySQL
Database = 'nft_project'
from datetime import datetime
import math

class Posts:
    def __init__( self , data ):
        self.id = data['id']
        self.contents = data['contents']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.image = ''
        self.poster_name = ''
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        # print(delta.days)
        # print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"
        
    @classmethod
    def add(cls,data):
        query = "INSERT INTO posts (contents,user_id,nft_id) VALUES ( %(contents)s,%(user_id)s,%(nft_id)s);"  
        return connectToMySQL(Database).query_db(query,data)
        