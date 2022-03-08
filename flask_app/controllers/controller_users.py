from flask import  render_template, request, redirect, session, flash
from flask_app.models.model_users import Users
from flask_app.models.model_friendships import link_friendship, dislink_friendship
from flask_app.models.model_posts import Posts
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

@app.route('/')
def login_page():
    if 'id' in session:
        del session['id']
    
    return render_template('login.html')

@app.route('/register')
def signup_page():
    if 'id' in session:
        del session['id']
    
    return render_template('signup.html')


@app.route('/registering', methods=['post'])
def registering():
    if not Users.validate(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password" : pw_hash
    }
    session['id'] = Users.add(data)
    
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')
    session['url'] = '/dashboard'
    # user = Users.get_one({'id':session['id']})
    user_with_friends = Users.get_users_all_friends({"id":session['id']})
    user_with_nft = Users.get_all_NFT({"id":session['id']})
    user_with_post = Users.get_all_posts({"id":session['id']})
    return render_template('dashboard.html',user=user_with_friends,user_with_nft=user_with_nft,user_with_post=user_with_post)


@app.route('/logining', methods=['post'])
def logining():
    data = {'email' : request.form['email']}
    user_db = Users.get_by_mail(data)
    if not Users.validate_login(request.form):
        return redirect('/')
    if not user_db:
        flash("Invalid Email/Password",'login_error')
        return redirect("/")
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash("Invalid Email/Password",'login_error')
        return redirect("/")    
    
    session['id'] = user_db.id
    return redirect('/dashboard')


@app.route('/redirecting_friend', methods = ['post'])
def friend_name():
    if 'id' not in session:
        return redirect('/')
    
    user = Users.get_by_name({'name':request.form['user_name']})
    if not user:
        flash("No such a user",'searching_error')
        return redirect(session['url'])
    
    id = user.id
    if id == session['id']:
        return redirect(f'/my_cyberoom/{id}')
    return redirect(f'/friend_cyberoom/{id}')


@app.route('/add_friend/<int:friend_id>')
def add_friend(friend_id):
    data ={
        'friend_id':friend_id,
        'user_id':session['id']
    }
    link_friendship(data)
    return redirect(session['url'])

@app.route('/dis_friend/<int:friend_id>')
def dis_friend(friend_id):
    data ={
        'friend_id':friend_id,
        'user_id':session['id']
    }
    dislink_friendship(data)
    return redirect(session['url'])

@app.route('/posting', methods=['post'])
def add_post():
    print(session['id'])
    data = {
        'nft_id':request.form['nft_id'],
        "user_id" :session['id'],
        'contents': request.form['contents']
    }
    Posts.add(data)
    return redirect('/dashboard')