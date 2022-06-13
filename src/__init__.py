from flask import Flask
import os
from users import signup
from sign_in import logon

HOST =  os.getenv("FLASK_HOST")
PORT = os.getenv("FLASK_PORT")

def create_app():
    app = Flask(__name__)
    app.register_blueprint(signup)
    app.register_blueprint(logon)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=True)
