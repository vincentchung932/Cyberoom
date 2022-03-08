from flask_app.config.mysqlconnection import connectToMySQL
Database = 'nft_project'
from solana_nfts import Client
import json
import requests

class Nfts:
    def __init__( self , data ):
        self.id = data['id']
        self.nft_json_address = data['nft_json_address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.address_id = data['address_id']
        self.image = ''
        self.name = ''
    

    @classmethod
    def add(cls,data):
        # data = {address_id, address}
        nft_json_addresses = cls.get_json_address(data['address'])
        # print(nft_json_addresses)
        for json_address in nft_json_addresses:
            # data['nft_json_address'] = json.dumps(json_address,ensure_ascii=False)
            data['nft_json_address'] = json_address
            # print('This is DATA!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print(data)
            query = "INSERT INTO nfts (nft_json_address,address_id) VALUES ( %(nft_json_address)s,%(address_id)s);"    
            connectToMySQL(Database).query_db(query,data)
        return 0
    
    @classmethod
    def get_user_all_nft(cls,data):
        return 0

    
    @staticmethod
    def get_json_address(address):
        nft_client = Client()
        nfts = nft_client.fetch_nfts_from_wallet_address(address)
        url = []
        for nft in nfts:
            json_link = requests.get(nft['arweave_metadata'])
            # print(nft["token_metadata"]["metadata"]["data"]["uri"])
            text = json_link.text
            # data = json.loads(text)
            url.append(text)
        return url




    

# print(url[0]["image"])
# print('-------------------------------------------------------------------------------')
# print(url[1]["image"])