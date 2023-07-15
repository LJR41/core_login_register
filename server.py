from flask_app import app
# ...server.py
from flask_app.controllers import user_controller
# ...server.py


if __name__=="__main__":
    app.run(debug=True)