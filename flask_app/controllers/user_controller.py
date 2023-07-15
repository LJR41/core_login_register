from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)
from flask_app import DATABASE


@app.route('/')
def home_display():
    if 'user_id'  in session:
        return redirect('/user/dashboard')
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def register():
    if not User.validate_user(request.form):
    # we redirect to the template with the form.
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data ={
        **request.form,
        'password': hashed_pass,
        'cpass' : hashed_pass
    }
    # ... do other things
    logged_user_id = User.create_user(data)
    session['user_id'] = logged_user_id
    return redirect('/user/dashboard')

@app.route('/user/dashboard')
def dashboard_display():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id' : session['user_id'],
    }
    logged_user = User.get_with_id(data)
    return render_template('dashboard.html', logged_user=logged_user)

@app.route('/user/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    potential_user = User.get_with_email(data)
    if not potential_user:
        flash("Invalid Credentials", 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(potential_user.password, request.form['password']):
        flash ('Invalid Credentials', 'log')
        return redirect('/')
    session['user_id'] = potential_user.id
    return redirect('/user/dashboard')

@app.route('/user/logout')
def logout():
    del session['user_id']
    return redirect('/')