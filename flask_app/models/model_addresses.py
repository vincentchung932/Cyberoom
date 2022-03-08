from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.model_nfts import Nfts
from flask import flash
Database = 'nft_project'
class Addresses:
    def __init__( self , data ):
        self.id = data['id']
        self.address = data['address']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_nft = []

    
    
    @classmethod
    def add(cls,data):
        query = "INSERT INTO addresses (address,user_id) VALUES ( %(address)s,%(user_id)s);"  
        # data1 = {address_id, address}
        address_id = connectToMySQL(Database).query_db(query,data)
        data1 ={
            'address_id':address_id,
            'address' : data["address"]
        }
        Nfts.add(data1)
        return address_id
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM addresses;"
        results = connectToMySQL(Database).query_db(query)
        all_addresses = []
        for one_address in results:
            all_addresses.append( cls(one_address) )
        
        if results:
            return all_addresses
        else:
            return []
        
    @classmethod
    def get_address_with_user_id(cls,data):
        query = "SELECT * FROM addresses WHERE user_id = %(user_id)s;"
        results = connectToMySQL(Database).query_db(query,data)
        all_addresses = []
        for one_address in results:
            all_addresses.append( cls(one_address) )
        
        if results:
            return all_addresses
        else:
            return []
        
    @staticmethod
    def validate(new):
        is_valid = True # we assume this is true
        all_address = Addresses.get_all()
        addresses = []
        for one_address in all_address:
            addresses.append(one_address.address)
        if new in addresses:
            flash("You already add this wallet.",'wallet_error')
            is_valid = False
            
        return is_valid