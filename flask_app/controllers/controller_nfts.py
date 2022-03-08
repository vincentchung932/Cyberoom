from flask import  render_template, request, redirect, session, flash
from flask_app.models.model_users import Users
from flask_app.models.model_nfts import Nfts
from flask_app.models.model_addresses import Addresses

from flask_app import app


@app.route('/my_cyberoom/<int:id>')
def display_my_nfts(id):
    if 'id' not in session:
        return redirect('/')
    session['url'] = f'/my_cyberoom/{id}'
    # user = Users.get_one({'id':session['id']})
    user_with_nft = Users.get_all_NFT({'id':session['id']})
    # user_with_friends = Users.get_users_all_friends({'id':session['id']})
    all_address = Addresses.get_address_with_user_id({'user_id':session['id']})

    return render_template('myroom.html',user_with_nft = user_with_nft,all_address=all_address)

@app.route('/add_address/<int:id>', methods=["post"])
def add_address(id):
    if 'id' not in session:
        return redirect('/') 
    if not Addresses.validate(request.form['address']):
        return redirect(f'/my_cyberoom/{id}')
    
    data = {
        **request.form,
        'user_id': id
    }
    Addresses.add(data)
    return redirect(f'/my_cyberoom/{id}')


@app.route('/friend_cyberoom/<int:id>')
def friend_room(id):
    if 'id' not in session:
        return redirect('/')
    session['url'] = f'/friend_cyberoom/{id}'
    user_with_nft = Users.get_all_NFT({'id':id})
    user_with_friends = Users.get_users_all_friends({'id':session['id']})
    all_address = Addresses.get_address_with_user_id({'user_id':id})
    check = False
    for friend in user_with_friends.friends:
        if friend.id == id:
            check =True
    return render_template('friend_room.html',user_with_nft = user_with_nft,all_address=all_address,check=check)