from flask import Flask
app = Flask(__name__)
app.secret_key = "vinland"
DATABASE = 'login_schema'