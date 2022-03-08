from flask_app.config.mysqlconnection import connectToMySQL
Database = 'nft_project'

def link_friendship(data):
    query = "INSERT INTO friendships(user_id,friend_id) Values (%(user_id)s,%(friend_id)s);"    
    connectToMySQL(Database).query_db(query,data)
    query = "INSERT INTO friendships(user_id,friend_id) Values (%(friend_id)s,%(user_id)s);"    
    connectToMySQL(Database).query_db(query,data)
    return 0


def dislink_friendship(data):
    query = "DELETE FROM friendships WHERE user_id=%(user_id)s and friend_id=%(friend_id)s;"    
    connectToMySQL(Database).query_db(query,data)
    query = "DELETE FROM friendships WHERE user_id=%(friend_id)s and friend_id=%(user_id)s;"    
    connectToMySQL(Database).query_db(query,data)
    return 