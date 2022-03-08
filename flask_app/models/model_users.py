# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
import re
import json
from flask import flash
from flask_app.models import model_nfts
from flask_app.models import model_posts

Database = 'nft_project'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Users:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_address = []
        self.nfts = []
        self.friends = []
        self.posts = []

    
    
    @classmethod
    def add(cls,data):
        query = "INSERT INTO users (name,email,password) VALUES ( %(name)s,%(email)s,%(password)s);"    
        return connectToMySQL(Database).query_db(query,data)
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(Database).query_db(query)
        all_users = []
        for one_user in results:
            all_users.append( cls(one_user) )
        
        if results:
            return all_users
        else:
            return []
        
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(Database).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return []

    @classmethod
    def get_by_mail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(Database).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return [] 
        
    @classmethod
    def get_by_name(cls,data):
        query = "SELECT * FROM users WHERE name = %(name)s;"
        results = connectToMySQL(Database).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return [] 
    
    @classmethod
    def get_all_NFT(cls,data):
        query = 'SELECT * FROM users LEFT JOIN addresses ON users.id = addresses.user_id LEFT JOIN nfts ON nfts.address_id = addresses.id where users.id = %(id)s;'
        results = connectToMySQL(Database).query_db(query,data)
        user = cls(results[0])
        for right_tab in results:
            nft_data = {
                'id':right_tab["nfts.id"],
                'nft_json_address':right_tab['nft_json_address'],
                "created_at" : right_tab["nfts.created_at"],
                "updated_at" : right_tab["nfts.updated_at"],
                "address_id" : right_tab["addresses.id"]
            }
            if nft_data['id']:
                one_nft = model_nfts.Nfts(nft_data)
                info = json.loads(right_tab['nft_json_address'])
                one_nft.name= info['name']
                one_nft.image = info['image']
                user.nfts.append(one_nft)
        return user
    
    @classmethod
    def get_users_all_friends(cls,data):
        query = 'SELECT * FROM users LEFT JOIN friendships ON users.id = friendships.user_id LEFT JOIN users AS friends ON friendships.friend_id = friends.id where users.id = %(id)s;'
        results = connectToMySQL(Database).query_db(query,data)
        user = cls(results[0])
        for right_tab in results:
            friend_data = {
                'id':right_tab["friends.id"],
                'name':right_tab['friends.name'],
                'email':right_tab['friends.email'],
                'password':right_tab['password'],
                "created_at" : right_tab["friendships.created_at"],
                "updated_at" : right_tab["friendships.updated_at"],
                
            }
            user.friends.append(cls(friend_data))
        return user
    
    @classmethod
    def get_all_posts(cls,data):
        query = 'SELECT * FROM users LEFT JOIN friendships ON users.id = friendships.user_id LEFT JOIN posts ON posts.user_id = friendships.friend_id LEFT JOIN nfts ON nfts.id = posts.nft_id where users.id = %(id)s ORDER BY posts.created_at DESC;'
        results = connectToMySQL(Database).query_db(query,data)
        user = cls(results[0])
        for right_tab in results:
            post_data = {
                'id':right_tab["posts.id"],
                'contents':right_tab['contents'],
                "created_at" : right_tab["posts.created_at"],
                "updated_at" : right_tab["posts.updated_at"],
            }
            one_post = model_posts.Posts(post_data)
            temp = cls.get_one({'id':right_tab['posts.user_id']}) 
            if temp:
                one_post.poster_name = cls.get_one({'id':right_tab['posts.user_id']}).name
                info = json.loads(right_tab['nft_json_address'])
                one_post.image = info['image']
                print(info['image'])
            user.posts.append(one_post)
        return user
    
    
    
    
    
    @staticmethod
    def validate(new):
        is_valid = True # we assume this is true
        all_email = Users.get_all()
        email_name = []
        for one_email in all_email:
            email_name.append(one_email.email)
        if len(new['name'])<2:
            flash("Name must be at least 2 char!",'reg_error')
            is_valid = False
        
        
        if not EMAIL_REGEX.match(new['email']):
            flash("Invalid email address!",'reg_error')
            is_valid = False
        if new['email'] in email_name:
            flash("This email address is already exsit",'reg_error')
            is_valid = False
        
        if len(new['password'])<8:
            flash("password must be at least 8 char!",'reg_error')
            is_valid = False
        
        if new['password'] != new['confirm_password']:
            flash("Password should be the same!",'reg_error')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(new):
        is_valid = True # we assume this is true
        all_email = Users.get_all()
        email_name = []
        for one_email in all_email:
            email_name.append(one_email.email)
        
        if not EMAIL_REGEX.match(new['email']):
            flash("The username you entered doesn't belong to an account. Please check your username and try again.",'login_error')
            is_valid = False
        
        
        return is_valid
    
    
