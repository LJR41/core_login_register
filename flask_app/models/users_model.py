# import the function that will return an instance of a connection
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
import re	# the regex module
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query= """
            INSERT INTO users (first_name,last_name,email,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
            """
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_with_id(cls,data):
        query= """
            SELECT * FROM users WHERE id = %(id)s
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_with_email(cls,data):
        query= """
            SELECT * FROM users WHERE email = %(email)s
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod 
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash("Please enter a first name", 'reg')
            is_valid = False
        elif len(data['first_name']) < 2:
            flash("First name must be at least 2 characters", 'reg')
            is_valid = False
        elif not data['first_name'].isalpha():
            flash('First name can only contain letters', 'reg')
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Please enter a last name", 'reg')
            is_valid = False
        elif len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", 'reg')
            is_valid = False
        elif not data['last_name'].isalpha():
            flash('Last name can only contain letters', 'reg')
            is_valid = False
        if len(data['email']) < 1:
            flash('Email is required', 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Email must be in proper format", 'reg')
            is_valid = False
        else: 
            potential_user = User.get_with_email({'email': data['email']})
            if potential_user:
                flash('Email is already in database.', 'reg')
                is_valid = False
        if len(data['password']) < 1:
            flash('password required', 'reg')
            is_valid=False
        elif len(data['password']) < 8:
            flash('password length must be 8 characters or more', 'reg')
            is_valid=False
        elif data['password'] != data['cpass']:
            flash('passwords do not match', 'reg')
            is_valid=False
        return is_valid